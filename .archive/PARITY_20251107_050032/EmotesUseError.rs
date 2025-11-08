//! Generated parser for EmotesUseError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EmotesUseError {

}

pub fn parse_EmotesUseError(payload: &str) -> Result<EmotesUseError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EmotesUseError {
    };
    
    Ok(result)
}
