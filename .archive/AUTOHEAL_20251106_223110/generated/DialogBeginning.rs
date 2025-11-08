// AUTO-GENERATED from retroproto Go: DialogBeginning
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogBeginning {
  pub nPCId: i64,
}

pub fn parse_DialogBeginning(payload: &str) -> Result<DialogBeginning, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(DialogBeginning { nPCId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn DialogBeginning_to_json(m: &DialogBeginning) -> Value { json!(m) }