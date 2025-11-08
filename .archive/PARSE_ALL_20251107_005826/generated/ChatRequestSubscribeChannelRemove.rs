// AUTO-GENERATED from retroproto Go: ChatRequestSubscribeChannelRemove
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatRequestSubscribeChannelRemove {
  pub channels: String,
}

pub fn parse_ChatRequestSubscribeChannelRemove(payload: &str) -> Result<ChatRequestSubscribeChannelRemove, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatRequestSubscribeChannelRemove { channels: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatRequestSubscribeChannelRemove_to_json(m: &ChatRequestSubscribeChannelRemove) -> Value { json!(m) }