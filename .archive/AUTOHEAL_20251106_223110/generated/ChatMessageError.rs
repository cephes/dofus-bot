// AUTO-GENERATED from retroproto Go: ChatMessageError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatMessageError {
  pub reason: String,
}

pub fn parse_ChatMessageError(payload: &str) -> Result<ChatMessageError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatMessageError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatMessageError_to_json(m: &ChatMessageError) -> Value { json!(m) }