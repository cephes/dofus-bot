// AUTO-GENERATED from retroproto Go: ItemsItemSetRemove
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsItemSetRemove {
  pub id: i64,
}

pub fn parse_ItemsItemSetRemove(payload: &str) -> Result<ItemsItemSetRemove, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsItemSetRemove { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsItemSetRemove_to_json(m: &ItemsItemSetRemove) -> Value { json!(m) }