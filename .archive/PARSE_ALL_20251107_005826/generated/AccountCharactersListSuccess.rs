// AUTO-GENERATED from retroproto Go: AccountCharactersListSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCharactersListSuccess {
  pub charactersCount: i64,
}

pub fn parse_AccountCharactersListSuccess(payload: &str) -> Result<AccountCharactersListSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCharactersListSuccess { charactersCount: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountCharactersListSuccess_to_json(m: &AccountCharactersListSuccess) -> Value { json!(m) }