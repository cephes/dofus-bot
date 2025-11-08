//! Generated parser for AksRPing
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AksRPing {
    /// Numeric value
    pub value: i64,
}

pub fn parse_AksRPing(payload: &str) -> Result<AksRPing, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AksRPing {
        value,    };
    
    Ok(result)
}
