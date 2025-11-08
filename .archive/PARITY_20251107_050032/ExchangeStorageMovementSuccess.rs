//! Generated parser for ExchangeStorageMovementSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeStorageMovementSuccess {

}

pub fn parse_ExchangeStorageMovementSuccess(payload: &str) -> Result<ExchangeStorageMovementSuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeStorageMovementSuccess {
    };
    
    Ok(result)
}
