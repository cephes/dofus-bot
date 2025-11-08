// AUTO-GENERATED from retroproto Go: ExchangePutInShedFromInventory
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInShedFromInventory {
  pub mountId: i64,
}

pub fn parse_ExchangePutInShedFromInventory(payload: &str) -> Result<ExchangePutInShedFromInventory, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInShedFromInventory { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInShedFromInventory_to_json(m: &ExchangePutInShedFromInventory) -> Value { json!(m) }