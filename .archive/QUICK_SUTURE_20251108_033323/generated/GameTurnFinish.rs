//! Generated parser for GameTurnFinish
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameTurnFinish {

}

pub fn parse_GameTurnFinish(payload: &str) -> Result<GameTurnFinish, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameTurnFinish { ..Default::default() };
    
    Ok(result)
}

