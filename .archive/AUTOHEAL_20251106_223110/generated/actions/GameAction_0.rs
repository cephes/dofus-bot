// AUTO-GENERATED Game Action Parser for code 0
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameAction_0 {
}

pub fn parse_GameAction_0(extra: &str) -> Result<GameAction_0, String> {
    let payload = extra.trim();
    Ok(GameAction_0 {
    })
}

pub fn GameAction_0_to_json(m: &GameAction_0) -> Value {
    serde_json::json!({
    })
}