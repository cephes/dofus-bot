// AUTO-GENERATED from retroproto Go: ChatRequestSubscribeChannelAdd
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatRequestSubscribeChannelAdd {
  pub channels: String,
}

pub fn parse_ChatRequestSubscribeChannelAdd(payload: &str) -> Result<ChatRequestSubscribeChannelAdd, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ChatRequestSubscribeChannelAdd { channels: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ChatRequestSubscribeChannelAdd_to_json(m: &ChatRequestSubscribeChannelAdd) -> Value { json!(m) }