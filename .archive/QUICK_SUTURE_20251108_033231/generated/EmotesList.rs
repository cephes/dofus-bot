//! Generated parser for EmotesList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct EmotesList {
    /// CSV list of integers
    pub emotes: Vec<i64>,
}

pub fn parse_EmotesList(payload: &str) -> Result<EmotesList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let emotes = common_decode::parse_i64_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = EmotesList {
        emotes,, ..Default::default()};
    
    Ok(result)
}

