// AUTO-GENERATED from retroproto Go: ItemsTool
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ItemsTool {
  pub jobId: i64,
}

pub fn parse_ItemsTool(payload: &str) -> Result<ItemsTool, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ItemsTool { jobId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ItemsTool_to_json(m: &ItemsTool) -> Value { json!(m) }