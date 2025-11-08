//! Generated parser for AccountFriendServerList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountFriendServerList {
    /// CSV list (JSON encoded)
    pub servers_characters: Vec<String>,
}

pub fn parse_AccountFriendServerList(payload: &str) -> Result<AccountFriendServerList, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let servers_characters = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountFriendServerList {
        servers_characters,    };
    
    Ok(result)
}
