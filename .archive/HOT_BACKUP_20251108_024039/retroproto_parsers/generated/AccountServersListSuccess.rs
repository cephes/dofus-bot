//! Generated parser for AccountServersListSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountServersListSuccess {
    /// Unknown type time
    pub subscription: String,
    /// CSV list (JSON encoded)
    pub servers_characters: Vec<typ>,
}

pub fn parse_AccountServersListSuccess(payload: &str) -> Result<AccountServersListSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let subscription = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let servers_characters = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountServersListSuccess {
        subscription,
        servers_characters,    };
    
    Ok(result)
}


