// AUTO-GENERATED from retroproto Go: InfosSendScreenInfo
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InfosSendScreenInfo {
  pub width: i64,
  pub height: i64,
  pub displayState: i64,
}

pub fn parse_InfosSendScreenInfo(payload: &str) -> Result<InfosSendScreenInfo, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(InfosSendScreenInfo { width: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), height: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), displayState: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn InfosSendScreenInfo_to_json(m: &InfosSendScreenInfo) -> Value { json!(m) }