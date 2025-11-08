// AUTO-GENERATED GameAction subparser for action code 1
// Source: GameActionsActionMovement from Go definitions

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct GameAction_1 {
    pub id: i64,
    pub sprite_id: i64,
}

pub fn parse_GameAction_1(payload: &str) -> Result<GameAction_1, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut m = GameAction_1::default();

    // Parse fields from semicolon-separated payload
    let mut part_idx = 0;
    if part_idx < parts.len() {
        let part = parts[part_idx].trim();
        if !part.is_empty() {
            m.id = part.parse().unwrap_or(0);
        }
        part_idx += 1;
    }

    if part_idx < parts.len() {
        let part = parts[part_idx].trim();
        if !part.is_empty() {
            m.sprite_id = part.parse().unwrap_or(0);
        }
        part_idx += 1;
    }

    Ok(m)
}
