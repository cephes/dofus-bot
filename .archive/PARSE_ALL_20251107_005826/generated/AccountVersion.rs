// AUTO-GENERATED from retroproto Go: AccountVersion
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountVersion {
  pub major: i64,
  pub minor: i64,
  pub patch: i64,
  pub beta: i64,
  pub streaming: bool,
  pub electron: bool,
}

pub fn parse_AccountVersion(payload: &str) -> Result<AccountVersion, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountVersion { major: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), minor: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), patch: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), beta: parts.get(3).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), streaming: parts.get(4).map(|s| *s == "1" || *s == "true").unwrap_or(false), electron: parts.get(5).map(|s| *s == "1" || *s == "true").unwrap_or(false) })
}

pub fn AccountVersion_to_json(m: &AccountVersion) -> Value { json!(m) }