//! Generated parser for GameActions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameActions {
    pub action_type: i64,
    /// Unknown type GameActionsActionMovement
    pub action_movement: String,
    /// Unknown type GameActionsActionLoadGameMap
    pub action_load_game_map: String,
    /// Unknown type GameActionsActionChallenge
    pub action_challenge: String,
    /// Unknown type GameActionsActionChallengeAccept
    pub action_challenge_accept: String,
    /// Unknown type GameActionsActionChallengeRefuse
    pub action_challenge_refuse: String,
    /// Unknown type GameActionsActionChallengeJoin
    pub action_challenge_join: String,
}

pub fn parse_GameActions(payload: &str) -> Result<GameActions, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let action_type = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let action_movement = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_load_game_map = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge_accept = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge_refuse = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let action_challenge_join = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = GameActions {
action_type: action_type,
action_movement: action_movement,
action_load_game_map: action_load_game_map,
action_challenge: action_challenge,
action_challenge_accept: action_challenge_accept,
action_challenge_refuse: action_challenge_refuse,
        action_challenge_join,  ..Default::default()};
    
    Ok(result)
}

