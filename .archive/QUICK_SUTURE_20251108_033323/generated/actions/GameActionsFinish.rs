//! Generated parser for GameActionsFinish
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameActionsFinish {

}

pub fn parse_GameActionsFinish(payload: &str) -> Result<GameActionsFinish, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameActionsFinish { ..Default::default() };
    
    Ok(result)
}

