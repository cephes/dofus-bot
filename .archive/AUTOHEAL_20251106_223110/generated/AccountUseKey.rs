// AUTO-GENERATED from retroproto Go: AccountUseKey
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountUseKey {
  pub id: i64,
}

pub fn parse_AccountUseKey(payload: &str) -> Result<AccountUseKey, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountUseKey { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountUseKey_to_json(m: &AccountUseKey) -> Value { json!(m) }