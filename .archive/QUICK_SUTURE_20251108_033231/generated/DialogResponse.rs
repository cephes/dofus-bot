//! Generated parser for DialogResponse
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct DialogResponse {
    pub question: i64,
    pub answer: i64,
}

pub fn parse_DialogResponse(payload: &str) -> Result<DialogResponse, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let question = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let answer = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = DialogResponse {
question: question,
        answer,, ..Default::default()};
    
    Ok(result)
}

