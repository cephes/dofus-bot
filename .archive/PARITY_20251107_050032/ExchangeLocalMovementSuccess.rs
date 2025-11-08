//! Generated parser for ExchangeLocalMovementSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeLocalMovementSuccess {

}

pub fn parse_ExchangeLocalMovementSuccess(payload: &str) -> Result<ExchangeLocalMovementSuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLocalMovementSuccess {
    };
    
    Ok(result)
}
