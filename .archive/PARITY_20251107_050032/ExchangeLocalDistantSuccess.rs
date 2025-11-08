//! Generated parser for ExchangeLocalDistantSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeLocalDistantSuccess {

}

pub fn parse_ExchangeLocalDistantSuccess(payload: &str) -> Result<ExchangeLocalDistantSuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLocalDistantSuccess {
    };
    
    Ok(result)
}
