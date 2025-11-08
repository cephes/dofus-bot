
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameFrameObject2 {}

pub fn parse_GameFrameObject2(payload: &str) -> Result<GameFrameObject2, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(GameFrameObject2{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for GameFrameObject2, got: {}", p));
        Ok(GameFrameObject2{})
    }
}
