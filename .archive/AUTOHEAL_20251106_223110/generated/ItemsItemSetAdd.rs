// AUTO-GENERATED from retroproto Go: ItemsItemSetAdd
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsItemSetAdd {
  pub id: i64,
  pub itemsTemplatesIds: String,
}

pub fn parse_ItemsItemSetAdd(payload: &str) -> Result<ItemsItemSetAdd, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsItemSetAdd { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), itemsTemplatesIds: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ItemsItemSetAdd_to_json(m: &ItemsItemSetAdd) -> Value { json!(m) }