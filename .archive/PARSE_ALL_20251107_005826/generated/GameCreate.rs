// AUTO-GENERATED from retroproto Go: GameCreate
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameCreate {
  pub type_: i64,
}

pub fn parse_GameCreate(payload: &str) -> Result<GameCreate, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameCreate { type_: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn GameCreate_to_json(m: &GameCreate) -> Value { json!(m) }