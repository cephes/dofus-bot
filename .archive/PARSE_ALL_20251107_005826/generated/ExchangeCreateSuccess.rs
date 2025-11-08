// AUTO-GENERATED from retroproto Go: ExchangeCreateSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeCreateSuccess {
  pub nPCBuy: String,
  pub paddock: String,
}

pub fn parse_ExchangeCreateSuccess(payload: &str) -> Result<ExchangeCreateSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeCreateSuccess { nPCBuy: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), paddock: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ExchangeCreateSuccess_to_json(m: &ExchangeCreateSuccess) -> Value { json!(m) }