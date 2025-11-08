use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsSendActionsActionChallengeAccept {
    pub challenger_id: String,
}

pub fn parse_GameActionsSendActionsActionChallengeAccept(payload: &str) -> Result<GameActionsSendActionsActionChallengeAccept, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let challenger_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsSendActionsActionChallengeAccept {
        challenger_id,
    })
}
