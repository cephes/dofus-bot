//! Generated parser for ExchangeKillMountInPark
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeKillMountInPark {

}

pub fn parse_ExchangeKillMountInPark(payload: &str) -> Result<ExchangeKillMountInPark, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeKillMountInPark {
    };
    
    Ok(result)
}
