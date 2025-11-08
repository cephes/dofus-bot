// AUTO-GENERATED from retroproto Go: DialogCreate
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogCreate {
  pub nPCId: i64,
}

pub fn parse_DialogCreate(payload: &str) -> Result<DialogCreate, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(DialogCreate { nPCId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn DialogCreate_to_json(m: &DialogCreate) -> Value { json!(m) }