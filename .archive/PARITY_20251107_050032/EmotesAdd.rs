//! Generated parser for EmotesAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EmotesAdd {

}

pub fn parse_EmotesAdd(payload: &str) -> Result<EmotesAdd, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EmotesAdd {
    };
    
    Ok(result)
}
