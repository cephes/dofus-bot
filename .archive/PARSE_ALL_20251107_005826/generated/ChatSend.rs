// AUTO-GENERATED from retroproto Go: ChatSend
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatSend {
  pub privateReceiver: String,
  pub message: String,
}

pub fn parse_ChatSend(payload: &str) -> Result<ChatSend, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatSend { privateReceiver: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), message: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatSend_to_json(m: &ChatSend) -> Value { json!(m) }