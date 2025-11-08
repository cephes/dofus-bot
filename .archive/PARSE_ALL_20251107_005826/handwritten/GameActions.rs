// AUTO-GENERATED GameActions dispatcher
use serde_json::Value;

// Import available action parsing functions from the generated actions module
use crate::retroproto_parsers::generated::actions::GameAction_1::{GameAction_1, parse_GameAction_1};
use crate::retroproto_parsers::generated::actions::GameAction_2::{GameAction_2, parse_GameAction_2};
use crate::retroproto_parsers::generated::actions::GameAction_900::{GameAction_900, parse_GameAction_900};
use crate::retroproto_parsers::generated::actions::GameAction_901::{GameAction_901, parse_GameAction_901};
use crate::retroproto_parsers::generated::actions::GameAction_902::{GameAction_902, parse_GameAction_902};
use crate::retroproto_parsers::generated::actions::GameAction_903::{GameAction_903, parse_GameAction_903};

#[derive(Debug, Clone, serde::Serialize)]
pub struct GameActions {
    /// The action code right after "GA" (before first ';'), e.g., 0, 1, ...
    pub action_code: i64,
    /// The parsed payload for typed actions, or raw string for unhandled actions.
    pub payload: serde_json::Value,
}

pub fn parse_game_actions(extra: &str) -> Result<GameActions, String> {
    // Expected format like: "0;1;121339587;aeVfeGgdjfcRgcofaw"
    let mut it = extra.splitn(2, ';');
    let code_str = it.next().ok_or("missing action_code")?.trim();
    let action_code = code_str.parse::<i64>()
        .map_err(|e| format!("invalid action_code: {e}"))?;
    let rest = it.next().unwrap_or("").to_string();
    
    // Route to appropriate subparser
    let payload = route_game_action(action_code, &rest)?;
    
    Ok(GameActions { action_code, payload })
}

pub fn game_actions_to_json(m: &GameActions) -> Value {
    serde_json::json!({
        "action_code": m.action_code,
        "payload": m.payload,
    })
}

/// Route game action to specific parser based on action code
pub fn route_game_action(action_code: i64, rest: &str) -> Result<serde_json::Value, String> {
    match action_code {
        1 => {
            // Movement action
            match parse_GameAction_1(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_1: {}", e)),
            }
        },
        2 => {
            // LoadGameMap action
            match parse_GameAction_2(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_2: {}", e)),
            }
        },
        900 => {
            // Challenge action
            match parse_GameAction_900(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_900: {}", e)),
            }
        },
        901 => {
            // ChallengeAccept action
            match parse_GameAction_901(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_901: {}", e)),
            }
        },
        902 => {
            // ChallengeRefuse action
            match parse_GameAction_902(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_902: {}", e)),
            }
        },
        903 => {
            // ChallengeJoin action
            match parse_GameAction_903(rest) {
                Ok(parsed) => Ok(serde_json::to_value(parsed).unwrap()),
                Err(e) => Err(format!("Failed to parse GameAction_903: {}", e)),
            }
        },
        _ => {
            // Unknown action code - return unparsed with metadata
            Ok(serde_json::json!({
                "action_code": action_code,
                "unparsed_rest": rest,
                "note": "Action-specific parser not available"
            }))
        }
    }
}