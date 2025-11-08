// AUTO-GENERATED from retroproto Go: ExchangeRequestError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeRequestError {
  pub reason: String,
}

pub fn parse_ExchangeRequestError(payload: &str) -> Result<ExchangeRequestError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeRequestError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ExchangeRequestError_to_json(m: &ExchangeRequestError) -> Value { json!(m) }