//! Generated parser for AccountHosts
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountHosts {
    /// CSV list (JSON encoded)
    pub value: Vec<typ>,
}

pub fn parse_AccountHosts(payload: &str) -> Result<AccountHosts, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let value = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountHosts {
        value,  ..Default::default()};
    
    Ok(result)
}

