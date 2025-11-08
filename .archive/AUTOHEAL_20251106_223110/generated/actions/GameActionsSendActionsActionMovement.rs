use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsSendActionsActionMovement {
    pub dir_and_cells: String,
}

pub fn parse_GameActionsSendActionsActionMovement(payload: &str) -> Result<GameActionsSendActionsActionMovement, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let dir_and_cells = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsSendActionsActionMovement {
        dir_and_cells,
    })
}
