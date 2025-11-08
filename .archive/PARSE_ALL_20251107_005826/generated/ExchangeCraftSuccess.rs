
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExchangeCraftSuccess {}

pub fn parse_ExchangeCraftSuccess(payload: &str) -> Result<ExchangeCraftSuccess, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(ExchangeCraftSuccess{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for ExchangeCraftSuccess, got: {}", p));
        Ok(ExchangeCraftSuccess{})
    }
}
