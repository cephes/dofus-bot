//! Generated parser for GameFrameObject2
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameFrameObject2 {

}

pub fn parse_GameFrameObject2(payload: &str) -> Result<GameFrameObject2, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameFrameObject2 {
    };
    
    Ok(result)
}
