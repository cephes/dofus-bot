
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GuildGetInfosBoosts {}

pub fn parse_GuildGetInfosBoosts(payload: &str) -> Result<GuildGetInfosBoosts, String> {
    // This Go message is struct{}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {
        Ok(GuildGetInfosBoosts{})
    } else {
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for GuildGetInfosBoosts, got: {}", p));
        Ok(GuildGetInfosBoosts{})
    }
}
