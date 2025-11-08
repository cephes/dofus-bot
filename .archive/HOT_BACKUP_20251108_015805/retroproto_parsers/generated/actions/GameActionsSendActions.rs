//! Generated parser for GameActionsSendActions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct GameActionsSendActions {
    pub action_type: i64,
    /// Unknown type GameActionsSendActionsActionMovement
    pub action_movement: String,
    /// Unknown type GameActionsSendActionsActionChallenge
    pub action_challenge: String,
    /// Unknown type GameActionsSendActionsActionChallengeAccept
    pub action_challenge_accept: String,
    /// Unknown type GameActionsSendActionsActionChallengeRefuse
    pub action_challenge_refuse: String,
}

pub fn parse_GameActionsSendActions(payload: &str) -> Result<GameActionsSendActions, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let action_type = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let action_movement = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge_accept = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge_refuse = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = GameActionsSendActions {
        action_type,
        action_movement,
        action_challenge,
        action_challenge_accept,
        action_challenge_refuse,    };
    
    Ok(result)
}

