// AUTO-GENERATED from retroproto Go: ChatServerMessage
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatServerMessage {
  pub message: String,
}

pub fn parse_ChatServerMessage(payload: &str) -> Result<ChatServerMessage, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatServerMessage { message: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatServerMessage_to_json(m: &ChatServerMessage) -> Value { json!(m) }