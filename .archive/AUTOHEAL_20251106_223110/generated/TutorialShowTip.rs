// AUTO-GENERATED from retroproto Go: TutorialShowTip
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TutorialShowTip {
  pub id: i64,
}

pub fn parse_TutorialShowTip(payload: &str) -> Result<TutorialShowTip, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(TutorialShowTip { id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn TutorialShowTip_to_json(m: &TutorialShowTip) -> Value { json!(m) }