//! Generated parser for GameTurnReady
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameTurnReady {

}

pub fn parse_GameTurnReady(payload: &str) -> Result<GameTurnReady, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameTurnReady {, ..Default::default()};
    
    Ok(result)
}

