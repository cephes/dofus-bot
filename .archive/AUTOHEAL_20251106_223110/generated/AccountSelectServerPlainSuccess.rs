// AUTO-GENERATED from retroproto Go: AccountSelectServerPlainSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSelectServerPlainSuccess {
  pub host: String,
  pub port: String,
  pub ticket: String,
}

pub fn parse_AccountSelectServerPlainSuccess(payload: &str) -> Result<AccountSelectServerPlainSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSelectServerPlainSuccess { host: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), port: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), ticket: parts.get(2).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSelectServerPlainSuccess_to_json(m: &AccountSelectServerPlainSuccess) -> Value { json!(m) }