//! Generated parser for AccountLoginSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountLoginSuccess {
    pub authorized: bool,
}

pub fn parse_AccountLoginSuccess(payload: &str) -> Result<AccountLoginSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let authorized = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = AccountLoginSuccess {
        authorized,, ..Default::default()};
    
    Ok(result)
}

