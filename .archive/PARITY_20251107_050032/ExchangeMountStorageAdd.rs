//! Generated parser for ExchangeMountStorageAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeMountStorageAdd {
    /// Unknown type typ
    pub data: String,
    pub new_born: bool,
}

pub fn parse_ExchangeMountStorageAdd(payload: &str) -> Result<ExchangeMountStorageAdd, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let data = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let new_born = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeMountStorageAdd {
        data,
        new_born,    };
    
    Ok(result)
}
