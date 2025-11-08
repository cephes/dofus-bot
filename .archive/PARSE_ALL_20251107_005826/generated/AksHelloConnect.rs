// AUTO-GENERATED from retroproto Go: AksHelloConnect
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AksHelloConnect {
  pub salt: String,
}

pub fn parse_AksHelloConnect(payload: &str) -> Result<AksHelloConnect, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AksHelloConnect { salt: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn AksHelloConnect_to_json(m: &AksHelloConnect) -> Value { json!(m) }