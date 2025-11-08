// AUTO-GENERATED from retroproto Go: AksServerMessage
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AksServerMessage {
  pub value: String,
}

pub fn parse_AksServerMessage(payload: &str) -> Result<AksServerMessage, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AksServerMessage { value: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AksServerMessage_to_json(m: &AksServerMessage) -> Value { json!(m) }