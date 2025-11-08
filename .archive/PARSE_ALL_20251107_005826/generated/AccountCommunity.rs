// AUTO-GENERATED from retroproto Go: AccountCommunity
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCommunity {
  pub id: i64,
}

pub fn parse_AccountCommunity(payload: &str) -> Result<AccountCommunity, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCommunity { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountCommunity_to_json(m: &AccountCommunity) -> Value { json!(m) }