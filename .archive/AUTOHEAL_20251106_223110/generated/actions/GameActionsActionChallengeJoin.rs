use serde::{Serialize, Deserialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameActionsActionChallengeJoin {
    pub challenger_id: String,
    pub error_reason: String,
}

pub fn parse_GameActionsActionChallengeJoin(payload: &str) -> Result<GameActionsActionChallengeJoin, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let challenger_id = parts.get(0).map(|s| s.to_string()).unwrap_or_default();
    let error_reason = parts.get(1).map(|s| s.to_string()).unwrap_or_default();
    Ok(GameActionsActionChallengeJoin {
        challenger_id,
        error_reason,
    })
}
