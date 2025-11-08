// AUTO-GENERATED from retroproto Go: ExchangePutInMountParkFromShed
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInMountParkFromShed {
  pub mountId: i64,
}

pub fn parse_ExchangePutInMountParkFromShed(payload: &str) -> Result<ExchangePutInMountParkFromShed, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInMountParkFromShed { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInMountParkFromShed_to_json(m: &ExchangePutInMountParkFromShed) -> Value { json!(m) }