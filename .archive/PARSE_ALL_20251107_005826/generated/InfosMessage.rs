// AUTO-GENERATED from retroproto Go: InfosMessage
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InfosMessage {
  pub chatId: i64,
}

pub fn parse_InfosMessage(payload: &str) -> Result<InfosMessage, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(InfosMessage { chatId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn InfosMessage_to_json(m: &InfosMessage) -> Value { json!(m) }