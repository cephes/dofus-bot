// AUTO-GENERATED from retroproto Go: AksRPing
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AksRPing {
  pub value: String,
}

pub fn parse_AksRPing(payload: &str) -> Result<AksRPing, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AksRPing { value: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AksRPing_to_json(m: &AksRPing) -> Value { json!(m) }