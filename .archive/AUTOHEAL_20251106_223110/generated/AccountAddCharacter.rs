// AUTO-GENERATED from retroproto Go: AccountAddCharacter
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountAddCharacter {
  pub name: String,
  pub class: i64,
  pub sex: i64,
  pub color1: String,
  pub color2: String,
  pub color3: String,
}

pub fn parse_AccountAddCharacter(payload: &str) -> Result<AccountAddCharacter, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };
  Ok(AccountAddCharacter { name: parts.get(0).map(|s| s.to_string()).unwrap_or_default(), class: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), sex: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), color1: parts.get(3).map(|s| s.to_string()).unwrap_or_default(), color2: parts.get(4).map(|s| s.to_string()).unwrap_or_default(), color3: parts.get(5).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountAddCharacter_to_json(m: &AccountAddCharacter) -> Value { json!(m) }