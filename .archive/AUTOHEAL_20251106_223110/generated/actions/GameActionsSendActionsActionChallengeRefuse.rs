use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsSendActionsActionChallengeRefuse {
    pub challenger_id: String,
}

pub fn parse_GameActionsSendActionsActionChallengeRefuse(payload: &str) -> Result<GameActionsSendActionsActionChallengeRefuse, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let challenger_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsSendActionsActionChallengeRefuse {
        challenger_id,
    })
}
