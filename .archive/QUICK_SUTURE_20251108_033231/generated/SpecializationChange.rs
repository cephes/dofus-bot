//! Generated parser for SpecializationChange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SpecializationChange {
    /// Numeric value
    pub value: i64,
}

pub fn parse_SpecializationChange(payload: &str) -> Result<SpecializationChange, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = SpecializationChange {
        value,, ..Default::default()};
    
    Ok(result)
}

