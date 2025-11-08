// AUTO-GENERATED from retroproto Go: DialogCreateSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogCreateSuccess {
  pub nPCId: i64,
}

pub fn parse_DialogCreateSuccess(payload: &str) -> Result<DialogCreateSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(DialogCreateSuccess { nPCId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn DialogCreateSuccess_to_json(m: &DialogCreateSuccess) -> Value { json!(m) }