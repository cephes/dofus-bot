// AUTO-GENERATED from retroproto Go: ExchangePutInShedFromMountPark
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInShedFromMountPark {
  pub mountId: i64,
}

pub fn parse_ExchangePutInShedFromMountPark(payload: &str) -> Result<ExchangePutInShedFromMountPark, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInShedFromMountPark { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInShedFromMountPark_to_json(m: &ExchangePutInShedFromMountPark) -> Value { json!(m) }