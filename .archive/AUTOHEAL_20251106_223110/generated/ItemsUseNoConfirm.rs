// AUTO-GENERATED from retroproto Go: ItemsUseNoConfirm
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsUseNoConfirm {
  pub id: i64,
  pub spriteId: i64,
  pub cell: i64,
}

pub fn parse_ItemsUseNoConfirm(payload: &str) -> Result<ItemsUseNoConfirm, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsUseNoConfirm { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), spriteId: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), cell: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsUseNoConfirm_to_json(m: &ItemsUseNoConfirm) -> Value { json!(m) }