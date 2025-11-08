//! Generated parser for GameFrameObjectExternal
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameFrameObjectExternal {

}

pub fn parse_GameFrameObjectExternal(payload: &str) -> Result<GameFrameObjectExternal, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameFrameObjectExternal {
    };
    
    Ok(result)
}
