//! Generated parser for ItemsAddError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsAddError {
    /// Unknown type u8
    pub reason: String,
}

pub fn parse_ItemsAddError(payload: &str) -> Result<ItemsAddError, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let reason = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ItemsAddError {
        reason,    };
    
    Ok(result)
}
