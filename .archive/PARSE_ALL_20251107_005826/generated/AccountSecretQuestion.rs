// AUTO-GENERATED from retroproto Go: AccountSecretQuestion
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSecretQuestion {
  pub value: String,
}

pub fn parse_AccountSecretQuestion(payload: &str) -> Result<AccountSecretQuestion, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSecretQuestion { value: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSecretQuestion_to_json(m: &AccountSecretQuestion) -> Value { json!(m) }