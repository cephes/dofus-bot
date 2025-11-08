// AUTO-GENERATED from retroproto Go: GameActionsSendActions
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameActionsSendActions {
  pub actionType: i64,
  pub actionMovement: String,
  pub actionChallenge: String,
  pub actionChallengeAccept: String,
  pub actionChallengeRefuse: String,
}

pub fn parse_GameActionsSendActions(payload: &str) -> Result<GameActionsSendActions, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameActionsSendActions { actionType: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), actionMovement: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), actionChallenge: parts.get(2).map(|s| s.to_string()).unwrap_or_default(), actionChallengeAccept: parts.get(3).map(|s| s.to_string()).unwrap_or_default(), actionChallengeRefuse: parts.get(4).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn GameActionsSendActions_to_json(m: &GameActionsSendActions) -> Value { json!(m) }