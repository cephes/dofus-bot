use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsSendActionsActionChallenge {
    pub challenged_id: String,
}

pub fn parse_GameActionsSendActionsActionChallenge(payload: &str) -> Result<GameActionsSendActionsActionChallenge, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let challenged_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsSendActionsActionChallenge {
        challenged_id,
    })
}
