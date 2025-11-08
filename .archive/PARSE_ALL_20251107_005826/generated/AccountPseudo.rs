// AUTO-GENERATED from retroproto Go: AccountPseudo
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountPseudo {
  pub value: String,
}

pub fn parse_AccountPseudo(payload: &str) -> Result<AccountPseudo, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountPseudo { value: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountPseudo_to_json(m: &AccountPseudo) -> Value { json!(m) }