use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameEffect {
    pub action_id: i64,
    pub effect_id: i64,
    pub unknown1: i64,
    pub unknown2: i64,
    pub unknown3: i64,
    pub unknown4: i64,
    pub unknown5: i64,
    pub caster_id: i64,
    pub target_cell: i64,
    pub value: i64,
}

fn p_i64(s: &str) -> i64 {
    let t = s.trim();
    if t.is_empty() { return 0; }
    t.parse::<i64>().unwrap_or(0)
}

pub fn parse_game_effect(extra: &str) -> Result<GameEffect, String> {
    // extra does NOT include the "GIE" prefix. It's the part after it.
    // Expect semicolon-separated 10 fields; empty tokens -> 0.
    let mut parts: Vec<&str> = extra.split(';').collect();
    // Some captures may end with trailing NUL — trim them.
    for p in parts.iter_mut() {
        *p = p.trim_matches('\0');
    }

    // pad to 10
    while parts.len() < 10 { parts.push(""); }

    Ok(GameEffect {
        action_id:   p_i64(parts[0]),
        effect_id:   p_i64(parts[1]),
        unknown1:    p_i64(parts[2]),
        unknown2:    p_i64(parts[3]),
        unknown3:    p_i64(parts[4]),
        unknown4:    p_i64(parts[5]),
        unknown5:    p_i64(parts[6]),
        caster_id:   p_i64(parts[7]),
        target_cell: p_i64(parts[8]),
        value:       p_i64(parts[9]),
    })
}

pub fn game_effect_to_json(m: &GameEffect) -> Value {
    serde_json::json!({
        "action_id":   m.action_id,
        "effect_id":   m.effect_id,
        "unknown1":    m.unknown1,
        "unknown2":    m.unknown2,
        "unknown3":    m.unknown3,
        "unknown4":    m.unknown4,
        "unknown5":    m.unknown5,
        "caster_id":   m.caster_id,
        "target_cell": m.target_cell,
        "value":       m.value,
    })
}