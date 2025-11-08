//! Generated parser for AccountSelectServerPlainSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountSelectServerPlainSuccess {
    pub host: String,
    pub port: String,
    pub ticket: String,
}

pub fn parse_AccountSelectServerPlainSuccess(payload: &str) -> Result<AccountSelectServerPlainSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let host = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let port = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let ticket = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountSelectServerPlainSuccess {
        host,
        port,
        ticket,    };
    
    Ok(result)
}
