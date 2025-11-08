// AUTO-GENERATED Game Action Parser for code 1
use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameAction_1 {
    pub dir_and_cells: Vec<String>,
}

pub fn parse_GameAction_1(extra: &str) -> Result<GameAction_1, String> {
    let payload = extra.trim();
    let cells: Vec<String> = if payload.is_empty() {
        vec![]
    } else {
        payload.chars()
            .collect::<Vec<_>>()
            .chunks(3)
            .map(|chunk| chunk.iter().collect::<String>())
            .collect()
    };
    Ok(GameAction_1 {
        dir_and_cells: cells,
    })
}

pub fn GameAction_1_to_json(m: &GameAction_1) -> Value {
    serde_json::json!({
        dir_and_cells: m.dir_and_cells,
    })
}
