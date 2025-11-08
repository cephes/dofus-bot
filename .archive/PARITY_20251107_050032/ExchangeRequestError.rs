//! Generated parser for ExchangeRequestError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeRequestError {
    /// Unknown type u8
    pub reason: String,
}

pub fn parse_ExchangeRequestError(payload: &str) -> Result<ExchangeRequestError, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let reason = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ExchangeRequestError {
        reason,    };
    
    Ok(result)
}
