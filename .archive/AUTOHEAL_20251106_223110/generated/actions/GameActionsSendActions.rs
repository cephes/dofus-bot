use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsSendActions {
    pub action_type: String,
    pub action_movement: String,
    pub action_challenge: String,
    pub action_challenge_accept: String,
    pub action_challenge_refuse: String,
}

pub fn parse_GameActionsSendActions(payload: &str) -> Result<GameActionsSendActions, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let action_type = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let action_movement = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge = parts.get(2).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge_accept = parts.get(3).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge_refuse = parts.get(4).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsSendActions {
        action_type,
        action_movement,
        action_challenge,
        action_challenge_accept,
        action_challenge_refuse,
    })
}
