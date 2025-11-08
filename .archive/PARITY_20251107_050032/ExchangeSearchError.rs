//! Generated parser for ExchangeSearchError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeSearchError {

}

pub fn parse_ExchangeSearchError(payload: &str) -> Result<ExchangeSearchError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeSearchError {
    };
    
    Ok(result)
}
