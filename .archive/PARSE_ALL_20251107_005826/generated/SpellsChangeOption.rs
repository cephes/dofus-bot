// AUTO-GENERATED from retroproto Go: SpellsChangeOption
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpellsChangeOption {
  pub canUseSeeAllSpell: bool,
}

pub fn parse_SpellsChangeOption(payload: &str) -> Result<SpellsChangeOption, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpellsChangeOption { canUseSeeAllSpell: parts.get(0).map(|s| *s == "1" || *s == "true").unwrap_or(false) })
}

pub fn SpellsChangeOption_to_json(m: &SpellsChangeOption) -> Value { json!(m) }