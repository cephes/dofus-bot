//! Generated parser for AccountVersion
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountVersion {
    pub major: i64,
    pub minor: i64,
    pub patch: i64,
    pub beta: i64,
    pub streaming: bool,
    pub electron: bool,
}

pub fn parse_AccountVersion(payload: &str) -> Result<AccountVersion, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let major = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let minor = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let patch = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let beta = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let streaming = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
        let electron = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = AccountVersion {
major: major,
minor: minor,
patch: patch,
beta: beta,
streaming: streaming,
        electron,, ..Default::default()};
    
    Ok(result)
}

