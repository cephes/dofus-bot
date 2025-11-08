// AUTO-GENERATED/UPDATED by tools/port_missing_parsers_from_go.py
#![allow(non_snake_case, non_camel_case_types, unused_imports)]
use serde_json::Value;


#[derive(Default, Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct GameActions {
    pub ActionType: i64,
    pub ActionMovement: String,
    pub ActionLoadGameMap: String,
    pub ActionChallenge: String,
    pub ActionChallengeAccept: String,
    pub ActionChallengeRefuse: String,
    pub ActionChallengeJoin: String,
}


fn to_i64(s: &str) -> i64 {
    s.trim().parse::<i64>().unwrap_or_default()
}
fn to_f64(s: &str) -> f64 {
    s.trim().parse::<f64>().unwrap_or_default()
}
fn to_bool(s: &str) -> bool {
    match s.trim() {
        "1" | "true" | "True" | "TRUE" => true,
        _ => false,
    }
}
fn split_csv(s: &str) -> Vec<&str> {
    if s.trim().is_empty() { return vec![]; }
    s.split(',').collect()
}


pub fn parse_GameActions(payload: &str) -> Result<GameActions, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut out = GameActions::default();
    let mut idx = 0usize;
    // field: ActionType : int -> i64
    out.ActionType = parts.get(idx).map(|s| to_i64(s)).unwrap_or_default();
    idx += 1;
    // field: ActionMovement : GameActionsActionMovement -> String
    out.ActionMovement = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    // field: ActionLoadGameMap : GameActionsActionLoadGameMap -> String
    out.ActionLoadGameMap = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    // field: ActionChallenge : GameActionsActionChallenge -> String
    out.ActionChallenge = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    // field: ActionChallengeAccept : GameActionsActionChallengeAccept -> String
    out.ActionChallengeAccept = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    // field: ActionChallengeRefuse : GameActionsActionChallengeRefuse -> String
    out.ActionChallengeRefuse = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    // field: ActionChallengeJoin : GameActionsActionChallengeJoin -> String
    out.ActionChallengeJoin = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();
    idx += 1;
    Ok(out)
}


pub fn GameActions_to_json(m: &GameActions) -> Value { serde_json::to_value(m).unwrap_or(Value::Null) }

