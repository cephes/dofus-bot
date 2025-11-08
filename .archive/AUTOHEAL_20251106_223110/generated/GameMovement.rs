// AUTO-GENERATED from retroproto Go: GameMovement
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameMovement {
  pub sprites: String,
}

pub fn parse_GameMovement(payload: &str) -> Result<GameMovement, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameMovement { sprites: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn GameMovement_to_json(m: &GameMovement) -> Value { json!(m) }