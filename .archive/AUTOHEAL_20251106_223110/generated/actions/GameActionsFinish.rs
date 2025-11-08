use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsFinish {

}

pub fn parse_GameActionsFinish(payload: &str) -> Result<GameActionsFinish, String> {
    let parts: Vec<&str> = payload.split(';').collect();

    Ok(GameActionsFinish {

    })
}
