// AUTO-GENERATED from retroproto Go: EmotesSetDirection
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotesSetDirection {
  pub dir: i64,
}

pub fn parse_EmotesSetDirection(payload: &str) -> Result<EmotesSetDirection, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(EmotesSetDirection { dir: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn EmotesSetDirection_to_json(m: &EmotesSetDirection) -> Value { json!(m) }