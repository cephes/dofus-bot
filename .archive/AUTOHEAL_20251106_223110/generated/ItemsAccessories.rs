// AUTO-GENERATED from retroproto Go: ItemsAccessories
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsAccessories {
  pub id: i64,
}

pub fn parse_ItemsAccessories(payload: &str) -> Result<ItemsAccessories, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsAccessories { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsAccessories_to_json(m: &ItemsAccessories) -> Value { json!(m) }