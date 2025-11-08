//! Generated parser for KeyKeySuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct KeyKeySuccess {

}

pub fn parse_KeyKeySuccess(payload: &str) -> Result<KeyKeySuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = KeyKeySuccess {
    };
    
    Ok(result)
}
