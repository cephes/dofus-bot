// AUTO-GENERATED from retroproto Go: AccountLoginError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountLoginError {
  pub reason: String,
  pub extra: String,
}

pub fn parse_AccountLoginError(payload: &str) -> Result<AccountLoginError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountLoginError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), extra: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountLoginError_to_json(m: &AccountLoginError) -> Value { json!(m) }