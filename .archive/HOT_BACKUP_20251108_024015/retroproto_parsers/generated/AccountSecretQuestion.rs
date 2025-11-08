//! Generated parser for AccountSecretQuestion
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountSecretQuestion {
    /// Numeric value
    pub value: i64,
}

pub fn parse_AccountSecretQuestion(payload: &str) -> Result<AccountSecretQuestion, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountSecretQuestion {
        value,    };
    
    Ok(result)
}


