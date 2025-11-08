//! Generated parser for AccountCredential
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountCredential {
    /// Name/label
    pub username: String,
    pub hash: String,
    pub crypto_method: i64,
}

pub fn parse_AccountCredential(payload: &str) -> Result<AccountCredential, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let username = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let hash = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let crypto_method = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountCredential {
username: username,
hash: hash,
        crypto_method,  ..Default::default()};
    
    Ok(result)
}

