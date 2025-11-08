//! Generated parser for AccountNewQueue
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountNewQueue {
    /// Position list
    pub position: Vec<i64>,
    pub total_abo: i64,
    pub total_non_abo: i64,
    pub subscriber: bool,
    /// Dofus ID
    pub queue_id: i64,
}

pub fn parse_AccountNewQueue(payload: &str) -> Result<AccountNewQueue, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let position = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
        let total_abo = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let total_non_abo = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let subscriber = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
        let queue_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountNewQueue {
        position,
        total_abo,
        total_non_abo,
        subscriber,
        queue_id,    };
    
    Ok(result)
}

