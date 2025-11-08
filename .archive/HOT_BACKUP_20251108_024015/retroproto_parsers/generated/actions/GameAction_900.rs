// AUTO-GENERATED GameAction subparser for action code 900
// Source: GameActionsActionChallenge from Go definitions

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct GameAction_900 {
    pub challenger_id: i64,
    pub challenged_id: i64,
}

pub fn parse_GameAction_900(payload: &str) -> Result<GameAction_900, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut m = GameAction_900::default();

    // Parse fields from semicolon-separated payload
    let mut part_idx = 0;
    if part_idx < parts.len() {
        let part = parts[part_idx].trim();
        if !part.is_empty() {
            m.challenger_id = part.parse().unwrap_or(0);
        }
        part_idx += 1;
    }

    if part_idx < parts.len() {
        let part = parts[part_idx].trim();
        if !part.is_empty() {
            m.challenged_id = part.parse().unwrap_or(0);
        }
        part_idx += 1;
    }

    Ok(m)
}


