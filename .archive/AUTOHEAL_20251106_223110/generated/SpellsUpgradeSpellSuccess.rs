// AUTO-GENERATED from retroproto Go: SpellsUpgradeSpellSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpellsUpgradeSpellSuccess {
  pub id: i64,
  pub level: i64,
}

pub fn parse_SpellsUpgradeSpellSuccess(payload: &str) -> Result<SpellsUpgradeSpellSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(SpellsUpgradeSpellSuccess { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), level: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn SpellsUpgradeSpellSuccess_to_json(m: &SpellsUpgradeSpellSuccess) -> Value { json!(m) }