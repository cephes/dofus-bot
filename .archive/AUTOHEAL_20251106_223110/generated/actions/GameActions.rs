use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActions {
    pub action_type: String,
    pub action_movement: String,
    pub action_load_game_map: String,
    pub action_challenge: String,
    pub action_challenge_accept: String,
    pub action_challenge_refuse: String,
    pub action_challenge_join: String,
}

pub fn parse_GameActions(payload: &str) -> Result<GameActions, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let action_type = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let action_movement = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    let action_load_game_map = parts.get(2).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge = parts.get(3).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge_accept = parts.get(4).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge_refuse = parts.get(5).map(|s| s.to_string()).unwrap_or_default();
    let action_challenge_join = parts.get(6).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActions {
        action_type,
        action_movement,
        action_load_game_map,
        action_challenge,
        action_challenge_accept,
        action_challenge_refuse,
        action_challenge_join,
    })
}
