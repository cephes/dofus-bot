// AUTO-GENERATED from retroproto Go: AccountCharacterSelectedSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountCharacterSelectedSuccess {
  pub id: i64,
  pub name: String,
  pub level: i64,
  pub sex: i64,
  pub gFXId: i64,
  pub color1: String,
  pub color2: String,
  pub color3: String,
}

pub fn parse_AccountCharacterSelectedSuccess(payload: &str) -> Result<AccountCharacterSelectedSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountCharacterSelectedSuccess { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), name: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), level: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), sex: parts.get(3).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), gFXId: parts.get(4).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), color1: parts.get(5).map(|s| s.to_string()).unwrap_or_default(), color2: parts.get(6).map(|s| s.to_string()).unwrap_or_default(), color3: parts.get(7).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AccountCharacterSelectedSuccess_to_json(m: &AccountCharacterSelectedSuccess) -> Value { json!(m) }