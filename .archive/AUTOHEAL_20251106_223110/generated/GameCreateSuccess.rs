// AUTO-GENERATED from retroproto Go: GameCreateSuccess
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameCreateSuccess {
  pub type_: i64,
}

pub fn parse_GameCreateSuccess(payload: &str) -> Result<GameCreateSuccess, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameCreateSuccess { type_: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn GameCreateSuccess_to_json(m: &GameCreateSuccess) -> Value { json!(m) }