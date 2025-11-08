//! Generated parser for GameGameOver
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameGameOver {

}

pub fn parse_GameGameOver(payload: &str) -> Result<GameGameOver, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameGameOver {
    };
    
    Ok(result)
}
