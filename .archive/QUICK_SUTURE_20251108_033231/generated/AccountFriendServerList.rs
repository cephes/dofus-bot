//! Generated parser for AccountFriendServerList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountFriendServerList {
    /// CSV list (JSON encoded)
    pub servers_characters: Vec<typ>,
}

pub fn parse_AccountFriendServerList(payload: &str) -> Result<AccountFriendServerList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let servers_characters = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountFriendServerList {
        servers_characters,, ..Default::default()};
    
    Ok(result)
}

