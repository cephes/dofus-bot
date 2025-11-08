use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionCancel {
    pub id: String,
    pub params: String,
}

pub fn parse_GameActionCancel(payload: &str) -> Result<GameActionCancel, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let params = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionCancel {
        id,
        params,
    })
}
