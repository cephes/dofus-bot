// FUTURE ENHANCEMENT: Use ids::spell_name() to enrich spell-related action payloads
// Example: if action_code relates to spell casting, lookup spell names using ids::spell_name(spell_id)
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
    /// Parse error if any
    pub parse_error: Option<String>,
}

pub fn parse_game_actions(extra: &str) -> Result<GameActions, String> {
    // Expected format like: "0;1;121339587;aeVfeGgdjfcRgcofaw"
    let mut it = extra.splitn(2, ';');
    let code_str = it.next().ok_or("missing action_code")?.trim();
    
    // More robust action code parsing with fallback
    let action_code = match code_str.parse::<i64>() {
        Ok(code) => code,
        Err(e) => {
            // Return a structured result with error info instead of failing
            let payload = serde_json::json!({
                "action_code_str": code_str,
                "parse_error": format!("invalid action_code: {}", e),
                "raw_rest": it.next().unwrap_or(""),
                "note": "Failed to parse action code as integer"
            });
            
            return Ok(GameActions {
                action_code: 0, // Safe default
                payload,
                parse_error: Some(format!("invalid action_code: {}", e))
            });
        }
    };
    
    let rest = it.next().unwrap_or("").to_string();
    
    // Route to appropriate subparser, but don't let it fail the whole parse
    let payload = match route_game_action(action_code, &rest) {
        Ok(parsed) => parsed,
        Err(e) => {
            // Return structured error instead of failing
            serde_json::json!({
                "action_code": action_code,
                "unparsed_rest": rest,
                "parse_error": e,
                "note": "Action-specific parser failed"
            })
        }
    };
    
    Ok(GameActions { action_code, payload, parse_error: None })
}

pub fn game_actions_to_json(m: &GameActions) -> Value {
    serde_json::json!({
        "action_code": m.action_code,
        "payload": m.payload,
        "parse_error": m.parse_error,
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