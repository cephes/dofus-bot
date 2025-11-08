// AUTO-GENERATED from retroproto Go: ExchangeBigStoreItemList
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeBigStoreItemList {
  pub itemTemplateId: i64,
}

pub fn parse_ExchangeBigStoreItemList(payload: &str) -> Result<ExchangeBigStoreItemList, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangeBigStoreItemList { itemTemplateId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangeBigStoreItemList_to_json(m: &ExchangeBigStoreItemList) -> Value { json!(m) }