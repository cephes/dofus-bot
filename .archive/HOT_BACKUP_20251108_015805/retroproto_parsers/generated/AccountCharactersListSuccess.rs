//! Generated parser for AccountCharactersListSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountCharactersListSuccess {
    /// Unknown type time
    pub subscription: String,
    /// Count/number
    pub characters_count: i32,
    /// CSV list (JSON encoded)
    pub characters: Vec<typ>,
}

pub fn parse_AccountCharactersListSuccess(payload: &str) -> Result<AccountCharactersListSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let subscription = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let characters_count = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let characters = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountCharactersListSuccess {
        subscription,
        characters_count,
        characters,    };
    
    Ok(result)
}

