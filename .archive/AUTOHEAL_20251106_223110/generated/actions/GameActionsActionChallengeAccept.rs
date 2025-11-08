use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsActionChallengeAccept {
    pub challenger_id: String,
    pub challenged_id: String,
}

pub fn parse_GameActionsActionChallengeAccept(payload: &str) -> Result<GameActionsActionChallengeAccept, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let challenger_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let challenged_id = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsActionChallengeAccept {
        challenger_id,
        challenged_id,
    })
}
