// AUTO-GENERATED from retroproto Go: ItemsRemove
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsRemove {
  pub id: i64,
}

pub fn parse_ItemsRemove(payload: &str) -> Result<ItemsRemove, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsRemove { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsRemove_to_json(m: &ItemsRemove) -> Value { json!(m) }