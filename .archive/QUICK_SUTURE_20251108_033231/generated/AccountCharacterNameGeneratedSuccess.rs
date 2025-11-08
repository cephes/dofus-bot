//! Generated parser for AccountCharacterNameGeneratedSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountCharacterNameGeneratedSuccess {
    /// Name/label
    pub name: String,
}

pub fn parse_AccountCharacterNameGeneratedSuccess(payload: &str) -> Result<AccountCharacterNameGeneratedSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let name = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountCharacterNameGeneratedSuccess {
        name,, ..Default::default()};
    
    Ok(result)
}

