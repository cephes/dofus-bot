// AUTO-GENERATED from retroproto Go: AccountCharacterNameGeneratedSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCharacterNameGeneratedSuccess {
  pub name: String,
}

pub fn parse_AccountCharacterNameGeneratedSuccess(payload: &str) -> Result<AccountCharacterNameGeneratedSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCharacterNameGeneratedSuccess { name: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountCharacterNameGeneratedSuccess_to_json(m: &AccountCharacterNameGeneratedSuccess) -> Value { json!(m) }