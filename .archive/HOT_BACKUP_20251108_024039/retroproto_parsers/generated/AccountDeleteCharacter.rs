//! Generated parser for AccountDeleteCharacter
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountDeleteCharacter {
    /// Dofus ID
    pub id: i64,
    pub secret_answer: String,
}

pub fn parse_AccountDeleteCharacter(payload: &str) -> Result<AccountDeleteCharacter, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let secret_answer = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountDeleteCharacter {
        id,
        secret_answer,    };
    
    Ok(result)
}


