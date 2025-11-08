// AUTO-GENERATED Game Action Parser for code 903
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameAction_903 {
    pub challenger_id: i64,
    pub error_reason: String,
}

pub fn parse_GameAction_903(extra: &str) -> Result<GameAction_903, String> {
    let payload = extra.trim();
    let parts: Vec<&str> = if payload.is_empty() {
        vec![]
    } else {
        payload.split(';').collect()
    };
    Ok(GameAction_903 {
        challenger_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
        error_reason: parts.get(1).map(|s| s.to_string()).unwrap_or_default(),
    })
}

pub fn GameAction_903_to_json(m: &GameAction_903) -> Value {
    serde_json::json!({
        challenger_id: m.challenger_id,
        error_reason: m.error_reason,
    })
}
