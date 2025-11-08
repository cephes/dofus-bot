// AUTO-GENERATED from retroproto Go: ExchangeRequest
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeRequest {
  pub type_: i64,
  pub id: i64,
  pub cell: i64,
}

pub fn parse_ExchangeRequest(payload: &str) -> Result<ExchangeRequest, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeRequest { type_: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), id: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), cell: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangeRequest_to_json(m: &ExchangeRequest) -> Value { json!(m) }