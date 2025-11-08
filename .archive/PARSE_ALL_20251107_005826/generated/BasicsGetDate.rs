
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BasicsGetDate {}

pub fn parse_BasicsGetDate(payload: &str) -> Result<BasicsGetDate, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(BasicsGetDate{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for BasicsGetDate, got: {}", p));
        Ok(BasicsGetDate{})
    }
}
