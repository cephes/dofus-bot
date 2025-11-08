//! Generated parser for GameActions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameActions {
    pub action_r_type: i64,
    /// Unknown type GameActionsActionMovement
    pub action_movement: String,
    /// Unknown type GameActionsActionLoadGameMap
    pub action_load_game_map: String,
    /// Unknown type GameActionsActionChallenge
    pub action_challenge: String,
    /// Unknown type GameActionsActionChallengeAccept
    pub action_challenge_accept: String,
    /// Unknown type GameActionsActionChallengeRefuse
    pub action_challenge_refr_use: String,
    /// Unknown type GameActionsActionChallengeJoin
    pub action_challenge_join: String,
}

pub fn parse_GameActions(payload: &str) -> Result<GameActions, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let action_r_type = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let action_movement = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_load_game_map = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge_accept = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge_refr_use = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let action_challenge_join = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = GameActions {
        action_r_type,
        action_movement,
        action_load_game_map,
        action_challenge,
        action_challenge_accept,
        action_challenge_refr_use,
        action_challenge_join,    };
    
    Ok(result)
}
