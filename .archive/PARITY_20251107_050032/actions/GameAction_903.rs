// AUTO-GENERATED GameAction subparser for action code 903
// Source: GameActionsActionChallengeJoin from Go definitions

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct GameAction_903 {
    pub challenger_id: i64,
    pub error_reason: char,
}

pub fn parse_GameAction_903(payload: &str) -> Result<GameAction_903, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut m = GameAction_903::default();

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
            m.error_reason = part.chars().next().unwrap_or('\0');
        }
        part_idx += 1;
    }

    Ok(m)
}
