// AUTO-GENERATED from retroproto Go: AccountLoginSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountLoginSuccess {
  pub authorized: bool,
}

pub fn parse_AccountLoginSuccess(payload: &str) -> Result<AccountLoginSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountLoginSuccess { authorized: parts.get(0).map(|s| *s == "1" || *s == "true").unwrap_or(false) })
}

pub fn AccountLoginSuccess_to_json(m: &AccountLoginSuccess) -> Value { json!(m) }