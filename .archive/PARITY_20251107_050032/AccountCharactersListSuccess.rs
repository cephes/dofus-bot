//! Generated parser for AccountCharactersListSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountCharactersListSuccess {
    /// Unknown type time
    pub subscription: String,
    /// Count/number
    pub characters_count: i32,
    /// CSV list (JSON encoded)
    pub characters: Vec<String>,
}

pub fn parse_AccountCharactersListSuccess(payload: &str) -> Result<AccountCharactersListSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let subscription = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let characters_count = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let characters = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountCharactersListSuccess {
        subscription,
        characters_count,
        characters,    };
    
    Ok(result)
}
