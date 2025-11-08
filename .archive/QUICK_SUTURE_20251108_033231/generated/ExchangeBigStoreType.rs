//! Generated parser for ExchangeBigStoreType
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeBigStoreType {
    /// Unknown type retrotyp
    pub item_type: String,
}

pub fn parse_ExchangeBigStoreType(payload: &str) -> Result<ExchangeBigStoreType, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_type = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ExchangeBigStoreType {
        item_type,, ..Default::default()};
    
    Ok(result)
}

