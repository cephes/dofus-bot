// AUTO-GENERATED from retroproto Go: GameActionCancel
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameActionCancel {
  pub id: i64,
  pub params: String,
}

pub fn parse_GameActionCancel(payload: &str) -> Result<GameActionCancel, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameActionCancel { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), params: parts.get(1).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn GameActionCancel_to_json(m: &GameActionCancel) -> Value { json!(m) }