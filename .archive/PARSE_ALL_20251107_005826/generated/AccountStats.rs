// AUTO-GENERATED from retroproto Go: AccountStats
use serde::{Serialize, Deserialize};
use serde_json::{Value, json};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccountStats {
  pub xP: i64,
  pub xPLow: i64,
  pub xPHigh: i64,
  pub kama: i64,
  pub bonusPoints: i64,
  pub bonusPointsSpell: i64,
  pub alignment: i64,
  pub fakeAlignment: i64,
  pub alignmentLevel: i64,
  pub grade: i64,
  pub honour: i64,
  pub disgrace: i64,
  pub alignmentEnabled: bool,
  pub lP: i64,
  pub lPMax: i64,
  pub energy: i64,
  pub energyMax: i64,
  pub initiative: i64,
  pub discernment: i64,
}

pub fn parse_AccountStats(payload: &str) -> Result<AccountStats, String> {
  let p = payload.trim_end_matches('\0');
  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split('|').collect() };

  Ok(AccountStats { xP: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), xPLow: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), xPHigh: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), kama: parts.get(3).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), bonusPoints: parts.get(4).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), bonusPointsSpell: parts.get(5).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), alignment: parts.get(6).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), fakeAlignment: parts.get(7).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), alignmentLevel: parts.get(8).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), grade: parts.get(9).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), honour: parts.get(10).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), disgrace: parts.get(11).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), alignmentEnabled: parts.get(12).map(|s| *s == "1" || *s == "true").unwrap_or(false), lP: parts.get(13).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), lPMax: parts.get(14).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), energy: parts.get(15).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), energyMax: parts.get(16).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), initiative: parts.get(17).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(), discernment: parts.get(18).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default() })
}

pub fn AccountStats_to_json(m: &AccountStats) -> Value { json!(m) }