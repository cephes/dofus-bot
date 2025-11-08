
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HousesShare {}

pub fn parse_HousesShare(payload: &str) -> Result<HousesShare, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(HousesShare{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for HousesShare, got: {}", p));
        Ok(HousesShare{})
    }
}
