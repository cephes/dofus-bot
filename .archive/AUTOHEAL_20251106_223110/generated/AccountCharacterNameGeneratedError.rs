// AUTO-GENERATED from retroproto Go: AccountCharacterNameGeneratedError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCharacterNameGeneratedError {
  pub reason: i64,
}

pub fn parse_AccountCharacterNameGeneratedError(payload: &str) -> Result<AccountCharacterNameGeneratedError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCharacterNameGeneratedError { reason: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountCharacterNameGeneratedError_to_json(m: &AccountCharacterNameGeneratedError) -> Value { json!(m) }