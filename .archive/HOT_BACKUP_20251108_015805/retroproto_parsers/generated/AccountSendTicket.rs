//! Generated parser for AccountSendTicket
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountSendTicket {
    pub ticket: String,
}

pub fn parse_AccountSendTicket(payload: &str) -> Result<AccountSendTicket, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let ticket = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountSendTicket {
        ticket,    };
    
    Ok(result)
}

