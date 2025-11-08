use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsActionMovement {
    pub id: String,
    pub sprite_id: String,
    pub dir_and_cells: String,
}

pub fn parse_GameActionsActionMovement(payload: &str) -> Result<GameActionsActionMovement, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let sprite_id = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    let dir_and_cells = parts.get(2).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsActionMovement {
        id,
        sprite_id,
        dir_and_cells,
    })
}
