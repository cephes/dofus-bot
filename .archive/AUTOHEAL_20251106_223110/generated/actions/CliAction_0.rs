// AUTO-GENERATED Game Action Parser for code 0
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct CliAction_0 {
}

pub fn parse_CliAction_0(extra: &str) -> Result<CliAction_0, String> {
    let payload = extra.trim();
    Ok(CliAction_0 {
    })
}

pub fn CliAction_0_to_json(m: &CliAction_0) -> Value {
    serde_json::json!({
    })
}