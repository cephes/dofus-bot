// AUTO-GENERATED from retroproto Go: ExchangeMountStorageRemove
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeMountStorageRemove {
  pub mountId: i64,
}

pub fn parse_ExchangeMountStorageRemove(payload: &str) -> Result<ExchangeMountStorageRemove, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeMountStorageRemove { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangeMountStorageRemove_to_json(m: &ExchangeMountStorageRemove) -> Value { json!(m) }