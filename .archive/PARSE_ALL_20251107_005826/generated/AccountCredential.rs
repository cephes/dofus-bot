// AUTO-GENERATED from retroproto Go: AccountCredential
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCredential {
  pub username: String,
  pub hash: String,
  pub cryptoMethod: i64,
}

pub fn parse_AccountCredential(payload: &str) -> Result<AccountCredential, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCredential { username: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), hash: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), cryptoMethod: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountCredential_to_json(m: &AccountCredential) -> Value { json!(m) }