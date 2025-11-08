//! Generated parser for EmotesDirection
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct EmotesDirection {
    /// Dofus ID
    pub id: i64,
    pub dir: i64,
}

pub fn parse_EmotesDirection(payload: &str) -> Result<EmotesDirection, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let dir = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = EmotesDirection {
id: id,
        dir,  ..Default::default()};
    
    Ok(result)
}

