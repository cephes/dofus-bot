// AUTO-GENERATED from retroproto Go: ItemsWeight
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsWeight {
  pub current: i64,
  pub max: i64,
}

pub fn parse_ItemsWeight(payload: &str) -> Result<ItemsWeight, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsWeight { current: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), max: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsWeight_to_json(m: &ItemsWeight) -> Value { json!(m) }