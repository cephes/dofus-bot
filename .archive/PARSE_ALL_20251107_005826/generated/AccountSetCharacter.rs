// AUTO-GENERATED from retroproto Go: AccountSetCharacter
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSetCharacter {
  pub id: i64,
}

pub fn parse_AccountSetCharacter(payload: &str) -> Result<AccountSetCharacter, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSetCharacter { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountSetCharacter_to_json(m: &AccountSetCharacter) -> Value { json!(m) }