//! Generated parser for ExchangeLeaveError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeLeaveError {

}

pub fn parse_ExchangeLeaveError(payload: &str) -> Result<ExchangeLeaveError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLeaveError {
    };
    
    Ok(result)
}
