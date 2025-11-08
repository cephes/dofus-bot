//! Generated parser for AccountSelectServerSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountSelectServerSuccess {
    pub host: String,
    pub port: String,
    pub ticket: String,
}

pub fn parse_AccountSelectServerSuccess(payload: &str) -> Result<AccountSelectServerSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let host = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let port = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let ticket = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountSelectServerSuccess {
        host,
        port,
        ticket,    };
    
    Ok(result)
}

