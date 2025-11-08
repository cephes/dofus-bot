// AUTO-GENERATED from retroproto Go: SpellsForget
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpellsForget {
  pub id: i64,
}

pub fn parse_SpellsForget(payload: &str) -> Result<SpellsForget, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpellsForget { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn SpellsForget_to_json(m: &SpellsForget) -> Value { json!(m) }