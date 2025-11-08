// AUTO-GENERATED from retroproto Go: ExchangeMountStorageAdd
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeMountStorageAdd {
  pub newBorn: bool,
}

pub fn parse_ExchangeMountStorageAdd(payload: &str) -> Result<ExchangeMountStorageAdd, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeMountStorageAdd { newBorn: parts.get(0).map(|s| *s == "1" || *s == "true").unwrap_or(false) })
}

pub fn ExchangeMountStorageAdd_to_json(m: &ExchangeMountStorageAdd) -> Value { json!(m) }