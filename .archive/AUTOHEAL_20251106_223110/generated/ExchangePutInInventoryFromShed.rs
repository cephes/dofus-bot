// AUTO-GENERATED from retroproto Go: ExchangePutInInventoryFromShed
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInInventoryFromShed {
  pub mountId: i64,
}

pub fn parse_ExchangePutInInventoryFromShed(payload: &str) -> Result<ExchangePutInInventoryFromShed, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInInventoryFromShed { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInInventoryFromShed_to_json(m: &ExchangePutInInventoryFromShed) -> Value { json!(m) }