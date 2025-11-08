// AUTO-GENERATED from retroproto Go: AccountNewLevel
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountNewLevel {
  pub level: i64,
}

pub fn parse_AccountNewLevel(payload: &str) -> Result<AccountNewLevel, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountNewLevel { level: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountNewLevel_to_json(m: &AccountNewLevel) -> Value { json!(m) }