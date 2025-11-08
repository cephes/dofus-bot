//! Generated parser for ExchangeLocalDistantError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeLocalDistantError {

}

pub fn parse_ExchangeLocalDistantError(payload: &str) -> Result<ExchangeLocalDistantError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLocalDistantError {
    };
    
    Ok(result)
}
