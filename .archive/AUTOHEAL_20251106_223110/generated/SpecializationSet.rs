// AUTO-GENERATED from retroproto Go: SpecializationSet
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpecializationSet {
  pub value: i64,
}

pub fn parse_SpecializationSet(payload: &str) -> Result<SpecializationSet, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpecializationSet { value: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn SpecializationSet_to_json(m: &SpecializationSet) -> Value { json!(m) }