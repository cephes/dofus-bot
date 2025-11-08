// AUTO-GENERATED from retroproto Go: BasicsSubscriberRestrictionAdd
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BasicsSubscriberRestrictionAdd {
  pub dialogId: i64,
}

pub fn parse_BasicsSubscriberRestrictionAdd(payload: &str) -> Result<BasicsSubscriberRestrictionAdd, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(BasicsSubscriberRestrictionAdd { dialogId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn BasicsSubscriberRestrictionAdd_to_json(m: &BasicsSubscriberRestrictionAdd) -> Value { json!(m) }