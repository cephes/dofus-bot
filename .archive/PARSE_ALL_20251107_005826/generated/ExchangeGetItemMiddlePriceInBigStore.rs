// AUTO-GENERATED from retroproto Go: ExchangeGetItemMiddlePriceInBigStore
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeGetItemMiddlePriceInBigStore {
  pub templateId: i64,
}

pub fn parse_ExchangeGetItemMiddlePriceInBigStore(payload: &str) -> Result<ExchangeGetItemMiddlePriceInBigStore, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeGetItemMiddlePriceInBigStore { templateId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangeGetItemMiddlePriceInBigStore_to_json(m: &ExchangeGetItemMiddlePriceInBigStore) -> Value { json!(m) }