// AUTO-GENERATED from retroproto Go: GameMapData
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameMapData {
  pub id: i64,
  pub name: String,
  pub key: String,
}

pub fn parse_GameMapData(payload: &str) -> Result<GameMapData, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(GameMapData { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), name: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), key: parts.get(2).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn GameMapData_to_json(m: &GameMapData) -> Value { json!(m) }