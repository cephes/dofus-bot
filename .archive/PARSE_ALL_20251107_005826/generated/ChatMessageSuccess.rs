// AUTO-GENERATED from retroproto Go: ChatMessageSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatMessageSuccess {
  pub id: i64,
  pub privateTo: bool,
  pub name: String,
  pub message: String,
}

pub fn parse_ChatMessageSuccess(payload: &str) -> Result<ChatMessageSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatMessageSuccess { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), privateTo: parts.get(1).map(|s| *s == "1" || *s == "true").unwrap_or(false), name: parts.get(2).map(|s| s.to_string()).unwrap_or_default(), message: parts.get(3).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatMessageSuccess_to_json(m: &ChatMessageSuccess) -> Value { json!(m) }