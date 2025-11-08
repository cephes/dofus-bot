//! Generated parser for AccountConfiguredPort
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountConfiguredPort {
    pub port: i64,
}

pub fn parse_AccountConfiguredPort(payload: &str) -> Result<AccountConfiguredPort, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let port = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountConfiguredPort {
        port,  ..Default::default()};
    
    Ok(result)
}

