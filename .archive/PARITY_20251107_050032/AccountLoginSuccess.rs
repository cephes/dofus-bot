//! Generated parser for AccountLoginSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountLoginSuccess {
    pub authorized: bool,
}

pub fn parse_AccountLoginSuccess(payload: &str) -> Result<AccountLoginSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let authorized = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
    
    // Create struct instance
    let result = AccountLoginSuccess {
        authorized,    };
    
    Ok(result)
}
