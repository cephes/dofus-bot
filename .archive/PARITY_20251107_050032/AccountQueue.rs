//! Generated parser for AccountQueue
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountQueue {
    /// Position list
    pub position: Vec<i64>,
}

pub fn parse_AccountQueue(payload: &str) -> Result<AccountQueue, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let position = common_decode::parse_i64_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountQueue {
        position,    };
    
    Ok(result)
}
