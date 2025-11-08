use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsStart {

}

pub fn parse_GameActionsStart(payload: &str) -> Result<GameActionsStart, String> {
    let parts: Vec<&str> = payload.split(';').collect();

    Ok(GameActionsStart {

    })
}
