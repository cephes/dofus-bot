// AUTO-GENERATED from retroproto Go: FightsCount
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FightsCount {
  pub value: i64,
}

pub fn parse_FightsCount(payload: &str) -> Result<FightsCount, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(FightsCount { value: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn FightsCount_to_json(m: &FightsCount) -> Value { json!(m) }