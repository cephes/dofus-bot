// AUTO-GENERATED from retroproto Go: GameMovementRemove
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameMovementRemove {
  pub id: i64,
}

pub fn parse_GameMovementRemove(payload: &str) -> Result<GameMovementRemove, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameMovementRemove { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn GameMovementRemove_to_json(m: &GameMovementRemove) -> Value { json!(m) }