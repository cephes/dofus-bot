// AUTO-GENERATED from retroproto Go: SpecializationChange
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpecializationChange {
  pub value: i64,
}

pub fn parse_SpecializationChange(payload: &str) -> Result<SpecializationChange, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpecializationChange { value: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn SpecializationChange_to_json(m: &SpecializationChange) -> Value { json!(m) }