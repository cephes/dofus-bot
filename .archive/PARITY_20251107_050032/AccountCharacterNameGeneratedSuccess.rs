//! Generated parser for AccountCharacterNameGeneratedSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountCharacterNameGeneratedSuccess {
    /// Name/label
    pub name: String,
}

pub fn parse_AccountCharacterNameGeneratedSuccess(payload: &str) -> Result<AccountCharacterNameGeneratedSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let name = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountCharacterNameGeneratedSuccess {
        name,    };
    
    Ok(result)
}
