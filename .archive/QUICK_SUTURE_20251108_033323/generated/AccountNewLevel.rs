//! Generated parser for AccountNewLevel
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountNewLevel {
    /// Level
    pub level: i32,
}

pub fn parse_AccountNewLevel(payload: &str) -> Result<AccountNewLevel, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let level = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountNewLevel {
        level,  ..Default::default()};
    
    Ok(result)
}

