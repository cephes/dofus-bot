// AUTO-GENERATED from retroproto Go: MountRename
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MountRename {
  pub name: String,
}

pub fn parse_MountRename(payload: &str) -> Result<MountRename, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(MountRename { name: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn MountRename_to_json(m: &MountRename) -> Value { json!(m) }