// AUTO-GENERATED from retroproto Go: MountRequestData
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MountRequestData {
  pub id: i64,
}

pub fn parse_MountRequestData(payload: &str) -> Result<MountRequestData, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(MountRequestData { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn MountRequestData_to_json(m: &MountRequestData) -> Value { json!(m) }