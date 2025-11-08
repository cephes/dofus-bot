//! Generated parser for SpellsMoveToUsed
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SpellsMoveToUsed {
    /// Dofus ID
    pub id: i64,
    /// Position list
    pub position: Vec<i64>,
}

pub fn parse_SpellsMoveToUsed(payload: &str) -> Result<SpellsMoveToUsed, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let position = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = SpellsMoveToUsed {
id: id,
        position,, ..Default::default()};
    
    Ok(result)
}

