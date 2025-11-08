//! Generated parser for AccountBoost
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountBoost {
    /// Dofus ID
    pub characteristic_id: i64,
    /// Numeric value
    pub amount: i64,
}

pub fn parse_AccountBoost(payload: &str) -> Result<AccountBoost, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let characteristic_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let amount = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AccountBoost {
        characteristic_id,
        amount,    };
    
    Ok(result)
}
