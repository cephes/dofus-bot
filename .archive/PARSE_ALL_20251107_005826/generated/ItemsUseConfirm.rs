// AUTO-GENERATED from retroproto Go: ItemsUseConfirm
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsUseConfirm {
  pub id: i64,
  pub spriteId: i64,
  pub cell: i64,
}

pub fn parse_ItemsUseConfirm(payload: &str) -> Result<ItemsUseConfirm, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsUseConfirm { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), spriteId: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), cell: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsUseConfirm_to_json(m: &ItemsUseConfirm) -> Value { json!(m) }