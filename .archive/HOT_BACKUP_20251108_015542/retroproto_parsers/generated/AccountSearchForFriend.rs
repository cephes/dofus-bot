//! Generated parser for AccountSearchForFriend
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountSearchForFriend {
    pub pseudo: String,
}

pub fn parse_AccountSearchForFriend(payload: &str) -> Result<AccountSearchForFriend, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let pseudo = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountSearchForFriend {
        pseudo,    };
    
    Ok(result)
}

