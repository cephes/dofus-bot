// AUTO-GENERATED from retroproto Go: ItemsDrop
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsDrop {
  pub id: i64,
  pub quantity: i64,
}

pub fn parse_ItemsDrop(payload: &str) -> Result<ItemsDrop, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsDrop { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), quantity: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsDrop_to_json(m: &ItemsDrop) -> Value { json!(m) }