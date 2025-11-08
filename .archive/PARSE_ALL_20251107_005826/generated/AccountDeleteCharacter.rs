// AUTO-GENERATED from retroproto Go: AccountDeleteCharacter
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountDeleteCharacter {
  pub id: i64,
  pub secretAnswer: String,
}

pub fn parse_AccountDeleteCharacter(payload: &str) -> Result<AccountDeleteCharacter, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountDeleteCharacter { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), secretAnswer: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountDeleteCharacter_to_json(m: &AccountDeleteCharacter) -> Value { json!(m) }