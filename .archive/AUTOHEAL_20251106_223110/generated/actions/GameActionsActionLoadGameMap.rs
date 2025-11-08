use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsActionLoadGameMap {
    pub sprite_id: String,
    pub cinematic: String,
}

pub fn parse_GameActionsActionLoadGameMap(payload: &str) -> Result<GameActionsActionLoadGameMap, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let sprite_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let cinematic = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsActionLoadGameMap {
        sprite_id,
        cinematic,
    })
}
