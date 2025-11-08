// AUTO-GENERATED from retroproto Go: MountEquipError
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MountEquipError {
  pub reason: String,
}

pub fn parse_MountEquipError(payload: &str) -> Result<MountEquipError, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(MountEquipError { reason: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn MountEquipError_to_json(m: &MountEquipError) -> Value { json!(m) }