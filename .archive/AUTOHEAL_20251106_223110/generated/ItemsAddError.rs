// AUTO-GENERATED from retroproto Go: ItemsAddError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsAddError {
  pub reason: String,
}

pub fn parse_ItemsAddError(payload: &str) -> Result<ItemsAddError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsAddError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ItemsAddError_to_json(m: &ItemsAddError) -> Value { json!(m) }