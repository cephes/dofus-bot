// AUTO-GENERATED from retroproto Go: AccountSearchForFriend
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSearchForFriend {
  pub pseudo: String,
}

pub fn parse_AccountSearchForFriend(payload: &str) -> Result<AccountSearchForFriend, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSearchForFriend { pseudo: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSearchForFriend_to_json(m: &AccountSearchForFriend) -> Value { json!(m) }