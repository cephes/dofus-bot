// AUTO-GENERATED from retroproto Go: AccountSelectServerError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSelectServerError {
  pub reason: String,
  pub extra: String,
}

pub fn parse_AccountSelectServerError(payload: &str) -> Result<AccountSelectServerError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSelectServerError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), extra: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSelectServerError_to_json(m: &AccountSelectServerError) -> Value { json!(m) }