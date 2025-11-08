
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameTurnOk {}

pub fn parse_GameTurnOk(payload: &str) -> Result<GameTurnOk, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(GameTurnOk{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for GameTurnOk, got: {}", p));
        Ok(GameTurnOk{})
    }
}
