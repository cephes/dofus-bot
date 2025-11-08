//! Generated parser for EmotesRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EmotesRemove {

}

pub fn parse_EmotesRemove(payload: &str) -> Result<EmotesRemove, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EmotesRemove {
    };
    
    Ok(result)
}
