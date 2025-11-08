//! Generated parser for ExchangeRequestReady
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeRequestReady {

}

pub fn parse_ExchangeRequestReady(payload: &str) -> Result<ExchangeRequestReady, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeRequestReady {
    };
    
    Ok(result)
}
