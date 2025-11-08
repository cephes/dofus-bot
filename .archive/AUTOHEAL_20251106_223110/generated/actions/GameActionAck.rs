use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionAck {
    pub id: String,
}

pub fn parse_GameActionAck(payload: &str) -> Result<GameActionAck, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionAck {
        id,
    })
}
