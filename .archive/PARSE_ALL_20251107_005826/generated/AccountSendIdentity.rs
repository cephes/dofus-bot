// AUTO-GENERATED from retroproto Go: AccountSendIdentity
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSendIdentity {
  pub id: String,
}

pub fn parse_AccountSendIdentity(payload: &str) -> Result<AccountSendIdentity, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSendIdentity { id: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSendIdentity_to_json(m: &AccountSendIdentity) -> Value { json!(m) }