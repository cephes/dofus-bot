//! Generated parser for AccountCredential
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountCredential {
    /// Name/label
    pub username: String,
    pub hash: String,
    pub crypto_method: i64,
}

pub fn parse_AccountCredential(payload: &str) -> Result<AccountCredential, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let username = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let hash = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let crypto_method = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AccountCredential {
        username,
        hash,
        crypto_method,    };
    
    Ok(result)
}
