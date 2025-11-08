//! Generated parser for AccountRestrictions
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountRestrictions {
    /// Unknown type typ
    pub restrictions: String,
}

pub fn parse_AccountRestrictions(payload: &str) -> Result<AccountRestrictions, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let restrictions = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountRestrictions {
        restrictions,    };
    
    Ok(result)
}
