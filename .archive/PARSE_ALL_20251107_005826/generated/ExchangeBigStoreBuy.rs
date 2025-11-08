// AUTO-GENERATED from retroproto Go: ExchangeBigStoreBuy
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeBigStoreBuy {
  pub itemId: i64,
  pub quantityIndex: i64,
  pub price: i64,
}

pub fn parse_ExchangeBigStoreBuy(payload: &str) -> Result<ExchangeBigStoreBuy, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeBigStoreBuy { itemId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), quantityIndex: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), price: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangeBigStoreBuy_to_json(m: &ExchangeBigStoreBuy) -> Value { json!(m) }