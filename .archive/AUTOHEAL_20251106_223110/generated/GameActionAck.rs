// AUTO-GENERATED from retroproto Go: GameActionAck
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameActionAck {
  pub id: i64,
}

pub fn parse_GameActionAck(payload: &str) -> Result<GameActionAck, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameActionAck { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn GameActionAck_to_json(m: &GameActionAck) -> Value { json!(m) }