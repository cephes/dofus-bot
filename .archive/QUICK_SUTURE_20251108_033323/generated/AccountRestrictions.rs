//! Generated parser for AccountRestrictions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountRestrictions {
    /// Unknown type typ
    pub restrictions: String,
}

pub fn parse_AccountRestrictions(payload: &str) -> Result<AccountRestrictions, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let restrictions = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountRestrictions {
        restrictions,  ..Default::default()};
    
    Ok(result)
}

