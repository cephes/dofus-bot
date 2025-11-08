// AUTO-GENERATED from retroproto Go: ExchangePutInCertificateFromShed
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangePutInCertificateFromShed {
  pub mountId: i64,
}

pub fn parse_ExchangePutInCertificateFromShed(payload: &str) -> Result<ExchangePutInCertificateFromShed, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(ExchangePutInCertificateFromShed { mountId: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn ExchangePutInCertificateFromShed_to_json(m: &ExchangePutInCertificateFromShed) -> Value { json!(m) }