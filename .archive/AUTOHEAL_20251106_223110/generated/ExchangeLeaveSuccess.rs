// AUTO-GENERATED from retroproto Go: ExchangeLeaveSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeLeaveSuccess {
  pub typePlayerExchange: bool,
}

pub fn parse_ExchangeLeaveSuccess(payload: &str) -> Result<ExchangeLeaveSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeLeaveSuccess { typePlayerExchange: parts.get(0).map(|s| *s == "1" || *s == "true").unwrap_or(false) })
}

pub fn ExchangeLeaveSuccess_to_json(m: &ExchangeLeaveSuccess) -> Value { json!(m) }