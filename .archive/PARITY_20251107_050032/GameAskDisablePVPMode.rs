//! Generated parser for GameAskDisablePVPMode
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameAskDisablePVPMode {

}

pub fn parse_GameAskDisablePVPMode(payload: &str) -> Result<GameAskDisablePVPMode, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameAskDisablePVPMode {
    };
    
    Ok(result)
}
