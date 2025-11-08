//! Generated parser for EmotesSetDirection
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EmotesSetDirection {
    pub dir: i64,
}

pub fn parse_EmotesSetDirection(payload: &str) -> Result<EmotesSetDirection, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let dir = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = EmotesSetDirection {
        dir,    };
    
    Ok(result)
}
