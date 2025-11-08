//! Generated parser for AccountSelectServerError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountSelectServerError {
    /// Unknown type rune
    pub reason: String,
    pub extra: String,
}

pub fn parse_AccountSelectServerError(payload: &str) -> Result<AccountSelectServerError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let reason = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let extra = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountSelectServerError {
reason: reason,
        extra,  ..Default::default()};
    
    Ok(result)
}

