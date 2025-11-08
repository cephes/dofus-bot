// AUTO-GENERATED from retroproto Go: AccountConfiguredPort
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountConfiguredPort {
  pub port: i64,
}

pub fn parse_AccountConfiguredPort(payload: &str) -> Result<AccountConfiguredPort, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountConfiguredPort { port: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountConfiguredPort_to_json(m: &AccountConfiguredPort) -> Value { json!(m) }