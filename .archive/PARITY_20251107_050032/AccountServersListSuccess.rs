//! Generated parser for AccountServersListSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountServersListSuccess {
    /// Unknown type time
    pub subscription: String,
    /// CSV list (JSON encoded)
    pub servers_characters: Vec<String>,
}

pub fn parse_AccountServersListSuccess(payload: &str) -> Result<AccountServersListSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let subscription = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let servers_characters = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountServersListSuccess {
        subscription,
        servers_characters,    };
    
    Ok(result)
}
