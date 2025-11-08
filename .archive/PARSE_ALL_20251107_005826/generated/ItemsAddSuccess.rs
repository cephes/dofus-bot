// AUTO-GENERATED from retroproto Go: ItemsAddSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsAddSuccess {
  pub items: String,
}

pub fn parse_ItemsAddSuccess(payload: &str) -> Result<ItemsAddSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsAddSuccess { items: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ItemsAddSuccess_to_json(m: &ItemsAddSuccess) -> Value { json!(m) }