//! Generated parser for ExchangeMovementPay
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeMovementPay {

}

pub fn parse_ExchangeMovementPay(payload: &str) -> Result<ExchangeMovementPay, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeMovementPay {
    };
    
    Ok(result)
}
