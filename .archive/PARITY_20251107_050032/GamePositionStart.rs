//! Generated parser for GamePositionStart
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GamePositionStart {

}

pub fn parse_GamePositionStart(payload: &str) -> Result<GamePositionStart, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GamePositionStart {
    };
    
    Ok(result)
}
