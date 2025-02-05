use core::str;
use std::sync::Arc;

use genvm_modules_interfaces::{ModuleError, ModuleResult};
use itertools::Itertools;
use serde::Deserialize;
use wiggle::GuestError;

use crate::{
    errors::*,
    ustar::SharedBytes,
    vm::{self, RunOk},
    AccountAddress, GenericAddress, MessageData,
};

use super::{base, common::*};

pub struct SingleVMData {
    pub conf: base::Config,
    pub message_data: MessageData,
    pub entrypoint: SharedBytes,
    pub supervisor: Arc<tokio::sync::Mutex<crate::vm::Supervisor>>,
}

pub struct Context {
    pub data: SingleVMData,
    pub shared_data: Arc<vm::SharedData>,
}

pub struct ContextVFS<'a> {
    pub(super) vfs: &'a mut VFS,
    pub(super) context: &'a mut Context,
}

pub(crate) mod generated {
    wiggle::from_witx!({
        witx: ["$CARGO_MANIFEST_DIR/src/wasi/witx/genlayer_sdk.witx"],
        errors: { errno => trappable Error },
        wasmtime: false,
        tracing: false,

        async: {
            genlayer_sdk::{
                call_contract, run_nondet, sandbox,
                get_webpage,
                exec_prompt, exec_prompt_id, eq_principle_prompt,
                deploy_contract, post_message,
                eth_send, eth_call,
                storage_read, storage_write,
            }
        },
    });

    wiggle::wasmtime_integration!({
        witx: ["$CARGO_MANIFEST_DIR/src/wasi/witx/genlayer_sdk.witx"],
        errors: { errno => trappable Error },
        target: self,
        tracing: false,

        async: {
            genlayer_sdk::{
                call_contract, run_nondet, sandbox,
                get_webpage,
                exec_prompt, exec_prompt_id, eq_principle_prompt,
                deploy_contract, post_message,
                eth_send, eth_call,
                storage_read, storage_write,
            }
        },
    });
}

impl crate::AccountAddress {
    fn read_from_mem(
        addr: &generated::types::Addr,
        mem: &mut wiggle::GuestMemory<'_>,
    ) -> Result<Self, generated::types::Error> {
        let cow = mem.as_cow(
            addr.ptr
                .as_array(crate::AccountAddress::len().try_into().unwrap()),
        )?;
        let mut ret = AccountAddress::zero();
        for (x, y) in ret.0.iter_mut().zip(cow.iter()) {
            *x = *y;
        }
        Ok(ret)
    }
}

impl crate::GenericAddress {
    fn read_from_mem(
        addr: &generated::types::FullAddr,
        mem: &mut wiggle::GuestMemory<'_>,
    ) -> Result<Self, generated::types::Error> {
        let cow = mem.as_cow(
            addr.ptr
                .as_array(crate::GenericAddress::len().try_into().unwrap()),
        )?;
        let mut ret = GenericAddress::zero();
        for (x, y) in ret.0.iter_mut().zip(cow.iter()) {
            *x = *y;
        }
        Ok(ret)
    }
}

impl generated::types::Bytes {
    #[allow(dead_code)]
    fn read_owned(
        &self,
        mem: &mut wiggle::GuestMemory<'_>,
    ) -> Result<Vec<u8>, generated::types::Error> {
        Ok(mem.as_cow(self.buf.as_array(self.buf_len))?.into_owned())
    }
}

impl Context {
    pub fn new(data: SingleVMData, shared_data: Arc<vm::SharedData>) -> Self {
        Self { data, shared_data }
    }
}

impl wiggle::GuestErrorType for generated::types::Errno {
    fn success() -> Self {
        Self::Success
    }
}

pub trait AddToLinkerFn<T> {
    fn call<'a>(&self, arg: &'a mut T) -> ContextVFS<'a>;
}

pub(super) fn add_to_linker_sync<'a, T: Send + 'static, F>(
    linker: &mut wasmtime::Linker<T>,
    f: F,
) -> anyhow::Result<()>
where
    F: AddToLinkerFn<T> + Copy + Send + Sync + 'static,
{
    #[derive(Clone, Copy)]
    struct Fwd<F>(F);

    impl<T, F> generated::AddGenlayerSdkToLinkerFn<T> for Fwd<F>
    where
        F: AddToLinkerFn<T> + Copy + Send + Sync + 'static,
    {
        fn call<'a>(&self, arg: &'a mut T) -> impl generated::genlayer_sdk::GenlayerSdk {
            self.0.call(arg)
        }
    }
    generated::add_genlayer_sdk_to_linker(linker, Fwd(f))?;
    Ok(())
}

#[derive(Debug)]
pub struct ContractReturn(pub Vec<u8>);

impl std::error::Error for ContractReturn {}

impl std::fmt::Display for ContractReturn {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Returned {:?}", self.0)
    }
}

impl From<GuestError> for generated::types::Error {
    fn from(err: GuestError) -> Self {
        use wiggle::GuestError::*;
        match err {
            InvalidFlagValue { .. } => generated::types::Errno::Inval.into(),
            InvalidEnumValue { .. } => generated::types::Errno::Inval.into(),
            // As per
            // https://github.com/WebAssembly/wasi/blob/main/legacy/tools/witx-docs.md#pointers
            //
            // > If a misaligned pointer is passed to a function, the function
            // > shall trap.
            // >
            // > If an out-of-bounds pointer is passed to a function and the
            // > function needs to dereference it, the function shall trap.
            //
            // so this turns OOB and misalignment errors into traps.
            PtrOverflow { .. } | PtrOutOfBounds { .. } | PtrNotAligned { .. } => {
                generated::types::Error::trap(err.into())
            }
            PtrBorrowed { .. } => generated::types::Errno::Fault.into(),
            InvalidUtf8 { .. } => generated::types::Errno::Ilseq.into(),
            TryFromIntError { .. } => generated::types::Errno::Overflow.into(),
            SliceLengthsDiffer { .. } => generated::types::Errno::Fault.into(),
            BorrowCheckerOutOfHandles { .. } => generated::types::Errno::Fault.into(),
            InFunc { err, .. } => generated::types::Error::from(*err),
        }
    }
}

impl From<std::num::TryFromIntError> for generated::types::Error {
    fn from(_err: std::num::TryFromIntError) -> Self {
        generated::types::Errno::Overflow.into()
    }
}

impl From<serde_json::Error> for generated::types::Error {
    fn from(err: serde_json::Error) -> Self {
        match err {
            _ => generated::types::Errno::Io.into(),
        }
    }
}

fn module_result_into_result<T>(zelf: ModuleResult<T>) -> Result<T, generated::types::Error> {
    match zelf {
        Ok(v) => Ok(v),
        Err(ModuleError::Recoverable(rec)) => {
            // TODO: fixme
            log::warn!(err:? = rec; "recoverable module error");
            Err(generated::types::Errno::Inval.into())
        }
        Err(ModuleError::Fatal(e)) => Err(generated::types::Error::trap(e)),
    }
}

impl ContextVFS<'_> {
    fn set_vm_run_result(
        &mut self,
        data: vm::RunOk,
    ) -> Result<(generated::types::Fd, usize), generated::types::Error> {
        let data = match data {
            RunOk::ContractError(e, cause) => {
                return Err(generated::types::Error::trap(
                    ContractError(e, cause).into(),
                ))
            }
            data => data,
        };
        let data: Box<[u8]> = data.as_bytes_iter().collect();
        let len = data.len();
        Ok((
            generated::types::Fd::from(self.vfs.place_content(
                FileContentsUnevaluated::from_contents(SharedBytes::new(data), 0),
            )),
            len,
        ))
    }
}

#[allow(unused_variables)]
#[async_trait::async_trait]
impl generated::genlayer_sdk::GenlayerSdk for ContextVFS<'_> {
    fn get_message_data(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
    ) -> Result<generated::types::ResultNow, generated::types::Error> {
        let res = serde_json::to_vec(&self.context.data.message_data)?;
        let res: SharedBytes = SharedBytes::new(res);
        let len = res.len().try_into()?;
        let fd = self
            .vfs
            .place_content(FileContentsUnevaluated::from_contents(res, 0));
        Ok(generated::types::ResultNow {
            len,
            file: generated::types::Fd::from(fd),
        })
    }

    fn get_entrypoint(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
    ) -> Result<generated::types::ResultNow, generated::types::Error> {
        let res = self.context.data.entrypoint.clone();
        let len = res.len().try_into()?;
        let fd = self
            .vfs
            .place_content(FileContentsUnevaluated::from_contents(res, 0));
        Ok(generated::types::ResultNow {
            len,
            file: generated::types::Fd::from(fd),
        })
    }

    fn rollback(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        message: wiggle::GuestPtr<str>,
    ) -> anyhow::Error {
        match super::common::read_string(mem, message) {
            Err(e) => e.into(),
            Ok(str) => Rollback(str).into(),
        }
    }

    fn contract_return(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        message: &generated::types::Bytes,
    ) -> anyhow::Error {
        let res = message.read_owned(mem);
        let Ok(res) = res else {
            return res.unwrap_err().into();
        };
        ContractReturn(res).into()
    }

    async fn get_webpage(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        config: wiggle::GuestPtr<str>,
        url: wiggle::GuestPtr<str>,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        let config_str = read_string(mem, config)?;
        let url_str = read_string(mem, url)?;

        let result_task = self
            .context
            .shared_data
            .modules
            .web
            .get_webpage(config_str, url_str);

        Ok(generated::types::Fd::from(self.vfs.place_content(
            FileContentsUnevaluated::from_task(result_task),
        )))
    }

    async fn exec_prompt(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        config: wiggle::GuestPtr<str>,
        prompt: wiggle::GuestPtr<str>,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        let config_str = read_string(mem, config)?;
        let prompt_str = read_string(mem, prompt)?;

        let result_task = self
            .context
            .shared_data
            .modules
            .llm
            .exec_prompt(config_str, prompt_str);

        Ok(generated::types::Fd::from(self.vfs.place_content(
            FileContentsUnevaluated::from_task(result_task),
        )))
    }

    async fn exec_prompt_id(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        id: u8,
        vars: wiggle::GuestPtr<str>,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        let vars_str = read_string(mem, vars)?;

        let result_task = self
            .context
            .shared_data
            .modules
            .llm
            .exec_prompt_id(id, vars_str);

        Ok(generated::types::Fd::from(self.vfs.place_content(
            FileContentsUnevaluated::from_task(result_task),
        )))
    }

    async fn eq_principle_prompt(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        id: u8,
        vars: wiggle::GuestPtr<str>,
    ) -> Result<generated::types::Success, generated::types::Error> {
        if self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        let vars_str = read_string(mem, vars)?;

        let res = self
            .context
            .shared_data
            .modules
            .llm
            .eq_principle_prompt(id, &vars_str)
            .await;

        let res = module_result_into_result(res)?;

        Ok((res as i32).try_into().unwrap())
    }

    async fn run_nondet(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        data_leader: &generated::types::Bytes,
        data_validator: &generated::types::Bytes,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if !self.context.data.conf.can_spawn_nondet {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }

        // relaxed reason: here is no actual race possible, only the deterministic vm can call it, and it has no concurrency
        let call_no = self
            .context
            .shared_data
            .nondet_call_no
            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);

        let leaders_res = {
            let supervisor = self.context.data.supervisor.clone();
            let mut supervisor = supervisor.lock().await;
            supervisor.host.get_leader_result(call_no)
        }
        .map_err(generated::types::Error::trap)?;

        let leaders_res = match (leaders_res, self.context.shared_data.is_sync) {
            (leaders_res, false) => leaders_res,
            (Some(leaders_res), true) => return self.set_vm_run_result(leaders_res).map(|x| x.0),
            (_, true) => {
                return Err(generated::types::Error::trap(anyhow::anyhow!(
                    "absent leader result in sync mode"
                )))
            }
        };

        let mut entrypoint = Vec::from(b"nondet!");
        match &leaders_res {
            None => {
                // we are the leader
                entrypoint.extend_from_slice(&0u32.to_le_bytes());
                let cow_leader = mem.as_cow(data_leader.buf.as_array(data_leader.buf_len))?;
                entrypoint.extend_from_slice(&cow_leader);
            }
            Some(leaders_res) => {
                // reserve size to rewrite later
                let entrypoint_size_off = entrypoint.len();
                entrypoint.extend_from_slice(&0u32.to_le_bytes());
                entrypoint.extend(leaders_res.as_bytes_iter());
                let written_len = (entrypoint.len() - 4 - entrypoint_size_off) as u32;
                entrypoint[entrypoint_size_off..entrypoint_size_off + 4]
                    .iter_mut()
                    .zip_eq(written_len.to_le_bytes())
                    .for_each(|(dst, src)| {
                        *dst = src;
                    });
                let cow_validator =
                    mem.as_cow(data_validator.buf.as_array(data_validator.buf_len))?;
                entrypoint.extend_from_slice(&cow_validator);
            }
        }
        let entrypoint = SharedBytes::new(entrypoint);

        let supervisor = self.context.data.supervisor.clone();

        let vm_data = SingleVMData {
            conf: base::Config {
                is_deterministic: false,
                can_read_storage: false,
                can_write_storage: false,
                can_spawn_nondet: false,
                can_call_others: false,
                can_send_messages: false,
                state_mode: crate::host::StorageType::Default,
            },
            message_data: self.context.data.message_data.clone(),
            entrypoint,
            supervisor: supervisor.clone(),
        };

        let my_res = self.context.spawn_and_run(&supervisor, vm_data).await;
        let my_res = ContractError::unwrap_res(my_res).map_err(generated::types::Error::trap)?;

        let ret_res = match leaders_res {
            None => {
                let mut supervisor = supervisor.lock().await;
                supervisor
                    .host
                    .post_result(call_no, &my_res)
                    .map_err(generated::types::Error::trap)?;
                Ok(my_res)
            }
            Some(leaders_res) => match my_res {
                RunOk::Return(v) if v == [16] => Ok(leaders_res),
                RunOk::Return(v) if v == [8] => {
                    Err(ContractError(format!("validator_disagrees call {}", call_no), None).into())
                }
                RunOk::ContractError(my_err, my_cause) => match leaders_res {
                    RunOk::ContractError(leader_err, leader_cause) => {
                        log::info!(
                            target: "vm",
                            event = "validator errored for leader error",
                            validator_error = my_err,
                            my_cause:? = my_cause,
                            leader_cause:? = leader_cause;
                            "AGREE"
                        );
                        Err(ContractError(leader_err, leader_cause).into())
                    }
                    _ => Err(ContractError(my_err, my_cause).into()),
                },
                _ => {
                    Err(ContractError(format!("validator_disagrees call {}", call_no), None).into())
                }
            },
        };
        let ret_res = ret_res.map_err(generated::types::Error::trap)?;
        self.set_vm_run_result(ret_res).map(|x| x.0)
    }

    async fn sandbox(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        data: &generated::types::Bytes,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        let mut entrypoint = Vec::from(b"sandbox!");
        let cow_data = mem.as_cow(data.buf.as_array(data.buf_len))?;
        entrypoint.extend_from_slice(&cow_data);

        let entrypoint = SharedBytes::new(entrypoint);

        let supervisor = self.context.data.supervisor.clone();

        let vm_data = SingleVMData {
            conf: base::Config {
                is_deterministic: self.context.data.conf.is_deterministic,
                can_read_storage: false,
                can_write_storage: false,
                can_spawn_nondet: false,
                can_call_others: false,
                can_send_messages: false,
                state_mode: crate::host::StorageType::Default,
            },
            message_data: self.context.data.message_data.clone(),
            entrypoint,
            supervisor: supervisor.clone(),
        };

        let my_res = self.context.spawn_and_run(&supervisor, vm_data).await;
        let my_res = ContractError::unwrap_res(my_res).map_err(generated::types::Error::trap)?;

        let data: Box<[u8]> = my_res.as_bytes_iter().collect();
        Ok(generated::types::Fd::from(self.vfs.place_content(
            FileContentsUnevaluated::from_contents(SharedBytes::new(data), 0),
        )))
    }

    async fn call_contract(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        account: &generated::types::Addr,
        calldata: &generated::types::Bytes,
        data: wiggle::GuestPtr<str>,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_call_others {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let called_contract_account = AccountAddress::read_from_mem(account, mem)?;
        let data = super::common::read_string(mem, data)?;
        #[derive(Deserialize)]
        struct Data {
            state: u8,
        }
        let data: Data =
            serde_json::from_str(&data).map_err(|_e| generated::types::Errno::Inval)?;
        let mut state_mode = crate::host::StorageType::try_from(data.state)
            .map_err(|_e| generated::types::Errno::Inval)?;
        if state_mode == crate::host::StorageType::Default {
            state_mode = crate::host::StorageType::LatestNonFinal;
        }
        let mut res_calldata = b"call!".to_vec();
        let calldata = calldata.buf.as_array(calldata.buf_len);
        res_calldata.extend(mem.as_cow(calldata)?.iter());
        let res_calldata = SharedBytes::new(res_calldata);

        let supervisor = self.context.data.supervisor.clone();

        let my_conf = self.context.data.conf;
        let my_data = self.context.data.message_data.clone();

        let vm_data = SingleVMData {
            conf: base::Config {
                is_deterministic: true,
                can_read_storage: my_conf.can_read_storage,
                can_write_storage: false,
                can_spawn_nondet: my_conf.can_spawn_nondet,
                can_call_others: my_conf.can_call_others,
                can_send_messages: my_conf.can_send_messages,
                state_mode,
            },
            message_data: MessageData {
                contract_account: called_contract_account,
                sender_account: my_data.sender_account, // FIXME: is that true?
                value: None,
                is_init: false,
                datetime: my_data.datetime,
                chain_id: my_data.chain_id,
                origin_account: my_data.origin_account,
            },
            entrypoint: res_calldata,
            supervisor: supervisor.clone(),
        };

        let res = self
            .context
            .spawn_and_run(&supervisor, vm_data)
            .await
            .map_err(generated::types::Error::trap)?;

        self.set_vm_run_result(res).map(|x| x.0)
    }

    async fn post_message(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        account: &generated::types::Addr,
        calldata: &generated::types::Bytes,
        data: wiggle::GuestPtr<str>,
    ) -> Result<(), generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_send_messages {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let address = AccountAddress::read_from_mem(account, mem)?;
        let calldata = calldata.read_owned(mem)?;
        let data = super::common::read_string(mem, data)?;

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;
        let res = supervisor
            .host
            .post_message(&address, &calldata, &data)
            .map_err(generated::types::Error::trap)?;
        Ok(())
    }

    async fn deploy_contract(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        calldata: &generated::types::Bytes,
        code: &generated::types::Bytes,
        data: wiggle::GuestPtr<str>,
    ) -> Result<(), generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_send_messages {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let calldata = calldata.read_owned(mem)?;
        let code = code.read_owned(mem)?;
        let data = super::common::read_string(mem, data)?;

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;
        let res = supervisor
            .host
            .deploy_contract(&calldata, &code, &data)
            .map_err(generated::types::Error::trap)?;
        Ok(())
    }

    async fn storage_read(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        slot: &generated::types::FullAddr,
        index: u32,
        buf: &generated::types::MutBytes,
    ) -> Result<(), generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_read_storage {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let dest_buf = buf.buf.as_array(buf.buf_len);

        let account = self.context.data.message_data.contract_account;

        let slot = GenericAddress::read_from_mem(slot, mem)?;
        let mem_size = buf.buf_len as usize;
        let mut vec = Vec::with_capacity(mem_size);
        unsafe { vec.set_len(mem_size) };

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;

        let res = supervisor.host.storage_read(
            self.context.data.conf.state_mode,
            account,
            slot,
            index,
            &mut vec,
        );

        res.map_err(|_e| generated::types::Errno::Io)?;
        mem.copy_from_slice(&vec, dest_buf)?;
        Ok(())
    }

    async fn storage_write(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        slot: &generated::types::FullAddr,
        index: u32,
        buf: &generated::types::Bytes,
    ) -> Result<(), generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_write_storage {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }

        let buf: Vec<u8> = buf.read_owned(mem)?;

        let account = self.context.data.message_data.contract_account;
        let slot = GenericAddress::read_from_mem(slot, mem)?;

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;

        let res = supervisor.host.storage_write(account, slot, index, &buf);

        res.map_err(|_e| generated::types::Errno::Io)?;
        Ok(())
    }

    async fn eth_send(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        account: &generated::types::Addr,
        calldata: &generated::types::Bytes,
    ) -> Result<(), generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_send_messages {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let address = AccountAddress::read_from_mem(account, mem)?;
        let calldata = calldata.read_owned(mem)?;

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;
        let res = supervisor
            .host
            .eth_send(address, &calldata)
            .map_err(generated::types::Error::trap)?;
        Ok(())
    }

    async fn eth_call(
        &mut self,
        mem: &mut wiggle::GuestMemory<'_>,
        account: &generated::types::Addr,
        calldata: &generated::types::Bytes,
    ) -> Result<generated::types::Fd, generated::types::Error> {
        if !self.context.data.conf.is_deterministic {
            return Err(generated::types::Errno::DeterministicViolation.into());
        }
        if !self.context.data.conf.can_call_others {
            return Err(generated::types::Errno::Forbidden.into());
        }

        let address = AccountAddress::read_from_mem(account, mem)?;
        let calldata = calldata.read_owned(mem)?;

        let supervisor = self.context.data.supervisor.clone();
        let mut supervisor = supervisor.lock().await;
        let res = supervisor
            .host
            .eth_call(address, &calldata)
            .map_err(generated::types::Error::trap)?;
        Ok(generated::types::Fd::from(self.vfs.place_content(
            FileContentsUnevaluated::from_contents(SharedBytes::new(res), 0),
        )))
    }
}

impl Context {
    pub fn log(&self) -> serde_json::Value {
        serde_json::json!({
            "config": &self.data.conf,
            "message": self.data.message_data
        })
    }

    async fn spawn_and_run(
        &mut self,
        supervisor: &Arc<tokio::sync::Mutex<crate::vm::Supervisor>>,
        essential_data: SingleVMData,
    ) -> vm::RunResult {
        let (mut vm, instance) = {
            let mut supervisor = supervisor.lock().await;
            let mut vm = supervisor.spawn(essential_data).await?;
            let instance = supervisor.apply_contract_actions(&mut vm).await?;
            (vm, instance)
        };
        vm.run(&instance).await
    }
}
