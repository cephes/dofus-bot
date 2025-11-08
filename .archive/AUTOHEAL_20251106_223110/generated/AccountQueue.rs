// AUTO-GENERATED from retroproto Go: AccountQueue
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountQueue {
  pub position: i64,
}

pub fn parse_AccountQueue(payload: &str) -> Result<AccountQueue, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountQueue { position: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountQueue_to_json(m: &AccountQueue) -> Value { json!(m) }