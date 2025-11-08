// AUTO-GENERATED from retroproto Go: AccountTicketResponseSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountTicketResponseSuccess {
  pub keyId: i64,
}

pub fn parse_AccountTicketResponseSuccess(payload: &str) -> Result<AccountTicketResponseSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountTicketResponseSuccess { keyId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountTicketResponseSuccess_to_json(m: &AccountTicketResponseSuccess) -> Value { json!(m) }