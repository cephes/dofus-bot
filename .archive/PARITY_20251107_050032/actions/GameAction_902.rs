// AUTO-GENERATED GameAction subparser for action code 902
// Source: GameActionsActionChallengeRefuse from Go definitions

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct GameAction_902 {
    pub challenger_id: i64,
    pub challenged_id: i64,
}

pub fn parse_GameAction_902(payload: &str) -> Result<GameAction_902, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut m = GameAction_902::default();

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
