//! Generated parser for ExchangeRequest
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeRequest {
    pub rr_type: i64,
    /// Dofus ID
    pub id: i64,
    /// Map cell number
    pub cell: i32,
}

pub fn parse_ExchangeRequest(payload: &str) -> Result<ExchangeRequest, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let rr_type = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let cell = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeRequest {
        rr_type,
        id,
        cell,    };
    
    Ok(result)
}
