// AUTO-GENERATED from retroproto Go: DialogResponse
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogResponse {
  pub question: i64,
  pub answer: i64,
}

pub fn parse_DialogResponse(payload: &str) -> Result<DialogResponse, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(DialogResponse { question: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), answer: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn DialogResponse_to_json(m: &DialogResponse) -> Value { json!(m) }