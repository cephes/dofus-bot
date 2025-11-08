// AUTO-GENERATED from retroproto Go: AccountSendTicket
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountSendTicket {
  pub ticket: String,
}

pub fn parse_AccountSendTicket(payload: &str) -> Result<AccountSendTicket, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountSendTicket { ticket: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountSendTicket_to_json(m: &AccountSendTicket) -> Value { json!(m) }