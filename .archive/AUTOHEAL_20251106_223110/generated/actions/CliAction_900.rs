// AUTO-GENERATED Game Action Parser for code 900
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct CliAction_900 {
    pub challenger_id: i64,
    pub challenged_id: i64,
}

pub fn parse_CliAction_900(extra: &str) -> Result<CliAction_900, String> {
    let payload = extra.trim();
    let parts: Vec<&str> = if payload.is_empty() {
        vec![]
    } else {
        payload.split(';').collect()
    };
    Ok(CliAction_900 {
        challenger_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
        challenged_id: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
    })
}

pub fn CliAction_900_to_json(m: &CliAction_900) -> Value {
    serde_json::json!({
        challenger_id: m.challenger_id,
        challenged_id: m.challenged_id,
    })
}
