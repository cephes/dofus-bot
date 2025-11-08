//! Generated parser for SpellsBoost
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SpellsBoost {
    /// Dofus ID
    pub id: i64,
}

pub fn parse_SpellsBoost(payload: &str) -> Result<SpellsBoost, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = SpellsBoost {
        id,, ..Default::default()};
    
    Ok(result)
}

