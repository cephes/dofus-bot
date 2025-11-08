// AUTO-GENERATED from retroproto Go: AccountSetServer
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSetServer {
  pub id: i64,
}

pub fn parse_AccountSetServer(payload: &str) -> Result<AccountSetServer, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSetServer { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountSetServer_to_json(m: &AccountSetServer) -> Value { json!(m) }