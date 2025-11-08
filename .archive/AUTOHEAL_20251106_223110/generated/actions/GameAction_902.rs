// AUTO-GENERATED Game Action Parser for code 902
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameAction_902 {
    pub challenger_id: i64,
    pub challenged_id: i64,
}

pub fn parse_GameAction_902(extra: &str) -> Result<GameAction_902, String> {
    let payload = extra.trim();
    let parts: Vec<&str> = if payload.is_empty() {
        vec![]
    } else {
        payload.split(';').collect()
    };
    Ok(GameAction_902 {
        challenger_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
        challenged_id: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
    })
}

pub fn GameAction_902_to_json(m: &GameAction_902) -> Value {
    serde_json::json!({
        challenger_id: m.challenger_id,
        challenged_id: m.challenged_id,
    })
}
