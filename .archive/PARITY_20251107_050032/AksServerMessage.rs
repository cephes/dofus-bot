//! Generated parser for AksServerMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AksServerMessage {
    /// Numeric value
    pub value: i64,
}

pub fn parse_AksServerMessage(payload: &str) -> Result<AksServerMessage, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AksServerMessage {
        value,    };
    
    Ok(result)
}
