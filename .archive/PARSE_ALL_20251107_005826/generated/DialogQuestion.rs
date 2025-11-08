// AUTO-GENERATED from retroproto Go: DialogQuestion
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DialogQuestion {
  pub question: i64,
  pub questionParams: String,
  pub answers: String,
}

pub fn parse_DialogQuestion(payload: &str) -> Result<DialogQuestion, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(DialogQuestion { question: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), questionParams: parts.get(1).map(|s| s.to_string()).unwrap_or_default(), answers: parts.get(2).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn DialogQuestion_to_json(m: &DialogQuestion) -> Value { json!(m) }