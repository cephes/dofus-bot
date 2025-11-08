//! Generated parser for BasicsAuthorizedCommandClear
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct BasicsAuthorizedCommandClear {

}

pub fn parse_BasicsAuthorizedCommandClear(payload: &str) -> Result<BasicsAuthorizedCommandClear, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = BasicsAuthorizedCommandClear {
    };
    
    Ok(result)
}
