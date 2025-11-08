// AUTO-GENERATED from retroproto Go: AccountCharacterAddError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCharacterAddError {
  pub reason: String,
}

pub fn parse_AccountCharacterAddError(payload: &str) -> Result<AccountCharacterAddError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCharacterAddError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountCharacterAddError_to_json(m: &AccountCharacterAddError) -> Value { json!(m) }