//! Generated parser for AccountVersion
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountVersion {
    pub major: i64,
    pub minor: i64,
    pub patch: i64,
    pub beta: i64,
    pub streaming: bool,
    pub electron: bool,
}

pub fn parse_AccountVersion(payload: &str) -> Result<AccountVersion, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let major = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let minor = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let patch = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let beta = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let streaming = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
        let electron = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
    
    // Create struct instance
    let result = AccountVersion {
        major,
        minor,
        patch,
        beta,
        streaming,
        electron,    };
    
    Ok(result)
}
