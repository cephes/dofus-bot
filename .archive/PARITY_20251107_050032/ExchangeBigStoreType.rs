//! Generated parser for ExchangeBigStoreType
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreType {
    /// Unknown type retrotyp
    pub item_r_type: String,
}

pub fn parse_ExchangeBigStoreType(payload: &str) -> Result<ExchangeBigStoreType, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_r_type = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ExchangeBigStoreType {
        item_r_type,    };
    
    Ok(result)
}
