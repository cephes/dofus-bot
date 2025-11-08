// AUTO-GENERATED from retroproto Go: SpellsMoveToUsed
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpellsMoveToUsed {
  pub id: i64,
  pub position: i64,
}

pub fn parse_SpellsMoveToUsed(payload: &str) -> Result<SpellsMoveToUsed, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpellsMoveToUsed { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), position: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn SpellsMoveToUsed_to_json(m: &SpellsMoveToUsed) -> Value { json!(m) }