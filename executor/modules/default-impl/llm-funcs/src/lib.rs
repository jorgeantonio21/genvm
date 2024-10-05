use anyhow::Result;
use genvm_modules_common::*;
use serde_derive::Deserialize;

use std::ffi::CStr;

use genvm_modules_common::interfaces::web_functions_api;

mod response;

genvm_modules_common::default_base_functions!(web_functions_api, Impl);

#[derive(Deserialize)]
#[serde(rename_all = "kebab-case")]
enum LLLMProvider {
    Ollama,
    Openai,
}

struct Impl {
    config: Config,
    openai_key: String,
}

impl Drop for Impl {
    fn drop(&mut self) {}
}

#[derive(Deserialize)]
struct Config {
    host: String,
    provider: LLLMProvider,
    model: String,
}

impl Impl {
    fn try_new(args: &CtorArgs) -> Result<Self> {
        let conf: &str = args.config()?;
        let config: Config = serde_json::from_str(conf)?;
        Ok(Impl {
            config,
            openai_key: std::env::var("OPENAIKEY").unwrap_or("".into()),
        })
    }

    fn call_llm(&mut self, gas: &mut u64, _config: &CStr, prompt: &CStr) -> Result<String> {
        let prompt = prompt.to_str()?;
        match self.config.provider {
            LLLMProvider::Ollama => {
                let request = serde_json::json!({
                    "model": &self.config.model,
                    "prompt": prompt,
                    "stream": false,
                });
                let mut res = isahc::send(
                    isahc::Request::post(&format!("{}/api/generate", self.config.host))
                        .body(serde_json::to_string(&request)?.as_bytes())?,
                )?;
                let res = response::read(&mut res)?;
                let val: serde_json::Value = serde_json::from_str(&res)?;
                let response = val
                    .as_object()
                    .and_then(|v| v.get("response"))
                    .and_then(|v| v.as_str())
                    .ok_or(anyhow::anyhow!("can't get response field {}", &res))?;
                let eval_duration = val
                    .as_object()
                    .and_then(|v| v.get("eval_duration"))
                    .and_then(|v| v.as_u64())
                    .ok_or(anyhow::anyhow!("can't get eval_duration field {}", &res))?;
                *gas -= (eval_duration << 4).min(*gas);
                Ok(response.into())
            }
            LLLMProvider::Openai => {
                let request = serde_json::json!({
                    "model": &self.config.model,
                    "messages": [{
                        "role": "user",
                        "content": prompt,
                    }],
                    "max_completion_tokens": 1000,
                    "stream": false,
                    "temperature": 0.7,
                });
                let mut res = isahc::send(
                    isahc::Request::post(&format!("{}/v1/chat/completions", self.config.host))
                        .header("Content-Type", "application/json")
                        .header("Authorization", &format!("Bearer {}", &self.openai_key))
                        .body(serde_json::to_string(&request)?.as_bytes())?,
                )?;
                let res = response::read(&mut res)?;
                let val: serde_json::Value = serde_json::from_str(&res)?;
                let response = val
                    .as_object()
                    .and_then(|v| v.get("choices"))
                    .and_then(|v| v.as_array())
                    .and_then(|v| v.get(0))
                    .and_then(|v| v.as_object())
                    .and_then(|v| v.get("message"))
                    .and_then(|v| v.as_object())
                    .and_then(|v| v.get("content"))
                    .and_then(|v| v.as_str())
                    .ok_or(anyhow::anyhow!("can't get response field {}", &res))?;
                let total_tokens = val
                    .as_object()
                    .and_then(|v| v.get("usage"))
                    .and_then(|v| v.as_object())
                    .and_then(|v| v.get("total_tokens"))
                    .and_then(|v| v.as_u64())
                    .ok_or(anyhow::anyhow!("can't get eval_duration field {}", &res))?;
                *gas -= (total_tokens << 8).min(*gas);
                Ok(response.into())
            }
        }
    }
}

#[no_mangle]
pub extern "C-unwind" fn call_llm(
    ctx: *const (),
    gas: &mut u64,
    config: *const u8,
    prompt: *const u8,
) -> interfaces::CStrResult {
    let ctx = get_ptr(ctx);
    let config = unsafe { CStr::from_ptr(config as *const std::ffi::c_char) };
    let prompt = unsafe { CStr::from_ptr(prompt as *const std::ffi::c_char) };
    ctx.call_llm(gas, config, prompt).into()
}
