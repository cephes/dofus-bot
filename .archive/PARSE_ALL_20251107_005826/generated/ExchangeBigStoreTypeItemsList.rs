// AUTO-GENERATED from retroproto Go: ExchangeBigStoreTypeItemsList
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeBigStoreTypeItemsList {
  pub itemTemplateIds: String,
}

pub fn parse_ExchangeBigStoreTypeItemsList(payload: &str) -> Result<ExchangeBigStoreTypeItemsList, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeBigStoreTypeItemsList { itemTemplateIds: parts.get(0).map(|s| s.to_string()).unwrap_or_default() })
}

pub fn ExchangeBigStoreTypeItemsList_to_json(m: &ExchangeBigStoreTypeItemsList) -> Value { json!(m) }