// AUTO-GENERATED from retroproto Go: EmotesList
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotesList {
  pub emotes: String,
}

pub fn parse_EmotesList(payload: &str) -> Result<EmotesList, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(EmotesList { emotes: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn EmotesList_to_json(m: &EmotesList) -> Value { json!(m) }