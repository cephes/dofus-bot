//! Generated parser for AccountNewQueue
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
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
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let position = common_decode::parse_i64_list(_fields.get(i).unwrap_or(&""));
        i += 1;
        let total_abo = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let total_non_abo = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let subscriber = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
        let queue_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AccountNewQueue {
        position,
        total_abo,
        total_non_abo,
        subscriber,
        queue_id,    };
    
    Ok(result)
}
