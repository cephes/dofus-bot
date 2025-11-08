//! Generated parser for AccountQueue
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountQueue {
    /// Position list
    pub position: Vec<i64>,
}

pub fn parse_AccountQueue(payload: &str) -> Result<AccountQueue, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let position = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountQueue {
        position,    };
    
    Ok(result)
}


