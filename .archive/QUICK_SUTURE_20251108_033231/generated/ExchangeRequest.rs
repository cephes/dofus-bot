//! Generated parser for ExchangeRequest
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeRequest {
    pub r#type: i64,
    /// Dofus ID
    pub id: i64,
    /// Map cell number
    pub cell: i32,
}

pub fn parse_ExchangeRequest(payload: &str) -> Result<ExchangeRequest, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let r#type = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let cell = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangeRequest {
        r#r#type: r#r#type: r#r#type: r#type,
id: id,
        cell,, ..Default::default()};
    
    Ok(result)
}

