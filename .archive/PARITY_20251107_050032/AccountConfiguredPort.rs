//! Generated parser for AccountConfiguredPort
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountConfiguredPort {
    pub port: i64,
}

pub fn parse_AccountConfiguredPort(payload: &str) -> Result<AccountConfiguredPort, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let port = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AccountConfiguredPort {
        port,    };
    
    Ok(result)
}
