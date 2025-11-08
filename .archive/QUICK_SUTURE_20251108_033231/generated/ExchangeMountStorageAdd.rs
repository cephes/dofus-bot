//! Generated parser for ExchangeMountStorageAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeMountStorageAdd {
    /// Unknown type typ
    pub data: String,
    pub new_born: bool,
}

pub fn parse_ExchangeMountStorageAdd(payload: &str) -> Result<ExchangeMountStorageAdd, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let data = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let new_born = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = ExchangeMountStorageAdd {
data: data,
        new_born,, ..Default::default()};
    
    Ok(result)
}

