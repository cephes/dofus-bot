//! Generated parser for GameClearAllEffect
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameClearAllEffect {

}

pub fn parse_GameClearAllEffect(payload: &str) -> Result<GameClearAllEffect, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameClearAllEffect {, ..Default::default()};
    
    Ok(result)
}

