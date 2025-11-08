//! Generated parser for GameActionsStart
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameActionsStart {

}

pub fn parse_GameActionsStart(payload: &str) -> Result<GameActionsStart, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameActionsStart { ..Default::default() };
    
    Ok(result)
}

