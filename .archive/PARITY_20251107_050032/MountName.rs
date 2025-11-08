//! Generated parser for MountName
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct MountName {
    /// Name/label
    pub name: String,
}

pub fn parse_MountName(payload: &str) -> Result<MountName, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let name = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = MountName {
        name,    };
    
    Ok(result)
}
