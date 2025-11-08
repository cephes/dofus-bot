// AUTO-GENERATED GameActions dispatcher
use serde_json::Value;

// Import available action parsing functions from the generated actions module
use crate::retroproto_parsers::generated::actions::{
    parse_GameActionAck,
    parse_GameActionCancel,
    parse_GameActions,
    parse_GameActionsActionChallenge,
    parse_GameActionsActionChallengeAccept,
    parse_GameActionsActionChallengeJoin,
    parse_GameActionsActionChallengeRefuse,
    parse_GameActionsActionLoadGameMap,
    parse_GameActionsActionMovement,
    parse_GameActionsFinish,
    parse_GameActionsSendActions,
    parse_GameActionsSendActionsActionChallenge,
    parse_GameActionsSendActionsActionChallengeAccept,
    parse_GameActionsSendActionsActionChallengeRefuse,
    parse_GameActionsSendActionsActionMovement,
    parse_GameActionsStart,
};

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameActions {
    /// The action code right after "GA" (before first ';'), e.g., 0, 1, ...
    pub action_code: i64,
    /// The rest of the payload (after the first ';'), kept as a raw string for now.
    pub rest: String,
}

pub fn parse_game_actions(extra: &str) -> Result<GameActions, String> {
    // Expected format like: "0;1;121339587;aeVfeGgdjfcRgcofaw"
    let mut it = extra.splitn(2, ';');
    let code_str = it.next().ok_or("missing action_code")?.trim();
    let action_code = code_str.parse::<i64>()
        .map_err(|e| format!("invalid action_code: {e}"))?;
    let rest = it.next().unwrap_or("").to_string();
    Ok(GameActions { action_code, rest })
}

pub fn game_actions_to_json(m: &GameActions) -> Value {
    serde_json::json!({
        "action_code": m.action_code,
        "rest": m.rest,
    })
}

/// Route game action to specific parser based on action code
pub fn route_game_action(action_code: i64, rest: &str) -> Result<serde_json::Value, String> {
    // For now, the generated parsers are based on Go struct names, not action codes.
    // This dispatcher provides basic unparsed handling until action code mapping is established.
    
    // Try to parse with available parsers (this is a placeholder - actual mapping needed)
    match action_code {
        _ => Ok(serde_json::json!({
            "action_code": action_code,
            "unparsed_rest": rest,
            "note": "Action-specific parser exists but needs code mapping"
        })),
    }
}