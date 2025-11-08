//! Generated parser for AccountCharacterNameGeneratedError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountCharacterNameGeneratedError {
    pub reason: i64,
}

pub fn parse_AccountCharacterNameGeneratedError(payload: &str) -> Result<AccountCharacterNameGeneratedError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let reason = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountCharacterNameGeneratedError {
        reason,  ..Default::default()};
    
    Ok(result)
}

