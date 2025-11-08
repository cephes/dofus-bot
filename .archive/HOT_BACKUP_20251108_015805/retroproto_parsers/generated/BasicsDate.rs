//! Generated parser for BasicsDate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct BasicsDate {
    pub year: i64,
    pub month: i64,
    pub day: i64,
}

pub fn parse_BasicsDate(payload: &str) -> Result<BasicsDate, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let year = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let month = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let day = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = BasicsDate {
        year,
        month,
        day,    };
    
    Ok(result)
}

