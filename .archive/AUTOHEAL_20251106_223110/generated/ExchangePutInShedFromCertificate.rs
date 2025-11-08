// AUTO-GENERATED from retroproto Go: ExchangePutInShedFromCertificate
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInShedFromCertificate {
  pub certificateId: i64,
}

pub fn parse_ExchangePutInShedFromCertificate(payload: &str) -> Result<ExchangePutInShedFromCertificate, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInShedFromCertificate { certificateId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInShedFromCertificate_to_json(m: &ExchangePutInShedFromCertificate) -> Value { json!(m) }