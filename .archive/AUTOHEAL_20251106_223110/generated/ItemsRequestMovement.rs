// AUTO-GENERATED from retroproto Go: ItemsRequestMovement
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsRequestMovement {
  pub id: i64,
  pub quantity: i64,
}

pub fn parse_ItemsRequestMovement(payload: &str) -> Result<ItemsRequestMovement, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsRequestMovement { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), quantity: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsRequestMovement_to_json(m: &ItemsRequestMovement) -> Value { json!(m) }