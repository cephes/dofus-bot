// AUTO-GENERATED Game Action Parser for code 2
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct CliAction_2 {
    pub sprite_id: i64,
    pub cinematic: String,
}

pub fn parse_CliAction_2(extra: &str) -> Result<CliAction_2, String> {
    let payload = extra.trim();
    let parts: Vec<&str> = if payload.is_empty() {
        vec![]
    } else {
        payload.split(';').collect()
    };
    Ok(CliAction_2 {
        sprite_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
        cinematic: parts.get(1).map(|s| s.to_string()).unwrap_or_default(),
    })
}

pub fn CliAction_2_to_json(m: &CliAction_2) -> Value {
    serde_json::json!({
        sprite_id: m.sprite_id,
        cinematic: m.cinematic,
    })
}
