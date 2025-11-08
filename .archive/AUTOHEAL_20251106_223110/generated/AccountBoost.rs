// AUTO-GENERATED from retroproto Go: AccountBoost
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountBoost {
  pub amount: i64,
}

pub fn parse_AccountBoost(payload: &str) -> Result<AccountBoost, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountBoost { amount: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountBoost_to_json(m: &AccountBoost) -> Value { json!(m) }