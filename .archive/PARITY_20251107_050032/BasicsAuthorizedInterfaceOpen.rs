//! Generated parser for BasicsAuthorizedInterfaceOpen
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct BasicsAuthorizedInterfaceOpen {

}

pub fn parse_BasicsAuthorizedInterfaceOpen(payload: &str) -> Result<BasicsAuthorizedInterfaceOpen, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = BasicsAuthorizedInterfaceOpen {
    };
    
    Ok(result)
}
