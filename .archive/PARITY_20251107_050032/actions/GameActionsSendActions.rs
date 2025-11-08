//! Generated parser for GameActionsSendActions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameActionsSendActions {
    pub action_r_type: i64,
    /// Unknown type GameActionsSendActionsActionMovement
    pub action_movement: String,
    /// Unknown type GameActionsSendActionsActionChallenge
    pub action_challenge: String,
    /// Unknown type GameActionsSendActionsActionChallengeAccept
    pub action_challenge_accept: String,
    /// Unknown type GameActionsSendActionsActionChallengeRefuse
    pub action_challenge_refr_use: String,
}

pub fn parse_GameActionsSendActions(payload: &str) -> Result<GameActionsSendActions, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let action_r_type = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let action_movement = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge_accept = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge_refr_use = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = GameActionsSendActions {
        action_r_type,
        action_movement,
        action_challenge,
        action_challenge_accept,
        action_challenge_refr_use,    };
    
    Ok(result)
}
