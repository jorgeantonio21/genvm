// This file is automatically generated, DO NOT EDIT
//
// To regenerate this file run the `crates/witx-bindgen` command

use core::fmt;
use core::mem::MaybeUninit;
#[repr(transparent)]
#[derive(Copy, Clone, Hash, Eq, PartialEq, Ord, PartialOrd)]
pub struct Errno(u32);
/// Success
pub const ERRNO_SUCCESS: Errno = Errno(0);
pub const ERRNO_DETERMINISTIC_VIOLATION: Errno = Errno(1);
pub const ERRNO_OVERFLOW: Errno = Errno(2);
pub const ERRNO_INVAL: Errno = Errno(3);
pub const ERRNO_FAULT: Errno = Errno(4);
pub const ERRNO_ILSEQ: Errno = Errno(5);
impl Errno {
    pub const fn raw(&self) -> u32 {
        self.0
    }

    pub fn name(&self) -> &'static str {
        match self.0 {
            0 => "SUCCESS",
            1 => "DETERMINISTIC_VIOLATION",
            2 => "OVERFLOW",
            3 => "INVAL",
            4 => "FAULT",
            5 => "ILSEQ",
            _ => unsafe { core::hint::unreachable_unchecked() },
        }
    }
    pub fn message(&self) -> &'static str {
        match self.0 {
            0 => "Success",
            1 => "",
            2 => "",
            3 => "",
            4 => "",
            5 => "",
            _ => unsafe { core::hint::unreachable_unchecked() },
        }
    }
}
impl fmt::Debug for Errno {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Errno")
            .field("code", &self.0)
            .field("name", &self.name())
            .field("message", &self.message())
            .finish()
    }
}
impl fmt::Display for Errno {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} (error {})", self.name(), self.0)
    }
}

#[cfg(feature = "std")]
extern crate std;
#[cfg(feature = "std")]
impl std::error::Error for Errno {}

pub type BytesLen = u32;
pub type None = u32;
pub unsafe fn rollback(message: &str) {
    genlayer_sdk::rollback(message.as_ptr() as i32, message.len() as i32);
}

pub unsafe fn get_calldata() -> Result<BytesLen, Errno> {
    let mut rp0 = MaybeUninit::<BytesLen>::uninit();
    let ret = genlayer_sdk::get_calldata(rp0.as_mut_ptr() as i32);
    match ret {
        0 => Ok(core::ptr::read(rp0.as_mut_ptr() as i32 as *const BytesLen)),
        _ => Err(Errno(ret as u32)),
    }
}

pub unsafe fn read_result(buf: *mut u8, len: u32) -> Result<BytesLen, Errno> {
    let mut rp0 = MaybeUninit::<BytesLen>::uninit();
    let ret = genlayer_sdk::read_result(buf as i32, len as i32, rp0.as_mut_ptr() as i32);
    match ret {
        0 => Ok(core::ptr::read(rp0.as_mut_ptr() as i32 as *const BytesLen)),
        _ => Err(Errno(ret as u32)),
    }
}

pub mod genlayer_sdk {
    #[link(wasm_import_module = "genlayer_sdk")]
    extern "C" {
        pub fn rollback(arg0: i32, arg1: i32) -> !;
        pub fn get_calldata(arg0: i32) -> i32;
        pub fn read_result(arg0: i32, arg1: i32, arg2: i32) -> i32;
    }
}
