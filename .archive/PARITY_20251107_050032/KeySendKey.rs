//! Generated parser for KeySendKey
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct KeySendKey {

}

pub fn parse_KeySendKey(payload: &str) -> Result<KeySendKey, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = KeySendKey {
    };
    
    Ok(result)
}
