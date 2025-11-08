// AUTO-GENERATED from retroproto Go: AccountSelectServerSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSelectServerSuccess {
  pub host: String,
  pub port: String,
  pub ticket: String,
}

pub fn parse_AccountSelectServerSuccess(payload: &str) -> Result<AccountSelectServerSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSelectServerSuccess { host: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), port: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), ticket: parts.get(2).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSelectServerSuccess_to_json(m: &AccountSelectServerSuccess) -> Value { json!(m) }