// AUTO-GENERATED Game Action Parser for code 901
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct CliAction_901 {
    pub challenger_id: i64,
    pub challenged_id: i64,
}

pub fn parse_CliAction_901(extra: &str) -> Result<CliAction_901, String> {
    let payload = extra.trim();
    let parts: Vec<&str> = if payload.is_empty() {
        vec![]
    } else {
        payload.split(';').collect()
    };
    Ok(CliAction_901 {
        challenger_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
        challenged_id: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
    })
}

pub fn CliAction_901_to_json(m: &CliAction_901) -> Value {
    serde_json::json!({
        challenger_id: m.challenger_id,
        challenged_id: m.challenged_id,
    })
}
