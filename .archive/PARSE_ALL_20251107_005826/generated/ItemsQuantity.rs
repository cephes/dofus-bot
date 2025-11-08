// AUTO-GENERATED from retroproto Go: ItemsQuantity
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsQuantity {
  pub id: i64,
  pub quantity: i64,
}

pub fn parse_ItemsQuantity(payload: &str) -> Result<ItemsQuantity, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsQuantity { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), quantity: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsQuantity_to_json(m: &ItemsQuantity) -> Value { json!(m) }