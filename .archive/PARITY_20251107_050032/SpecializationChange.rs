//! Generated parser for SpecializationChange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct SpecializationChange {
    /// Numeric value
    pub value: i64,
}

pub fn parse_SpecializationChange(payload: &str) -> Result<SpecializationChange, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = SpecializationChange {
        value,    };
    
    Ok(result)
}
