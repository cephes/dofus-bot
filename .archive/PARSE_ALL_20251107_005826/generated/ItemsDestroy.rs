// AUTO-GENERATED from retroproto Go: ItemsDestroy
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsDestroy {
  pub id: i64,
  pub quantity: i64,
}

pub fn parse_ItemsDestroy(payload: &str) -> Result<ItemsDestroy, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsDestroy { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), quantity: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsDestroy_to_json(m: &ItemsDestroy) -> Value { json!(m) }