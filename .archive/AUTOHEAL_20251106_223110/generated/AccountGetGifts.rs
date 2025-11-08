// AUTO-GENERATED from retroproto Go: AccountGetGifts
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountGetGifts {
  pub lang: String,
}

pub fn parse_AccountGetGifts(payload: &str) -> Result<AccountGetGifts, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountGetGifts { lang: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountGetGifts_to_json(m: &AccountGetGifts) -> Value { json!(m) }