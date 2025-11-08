//! Generated parser for AccountDeleteCharacter
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountDeleteCharacter {
    /// Dofus ID
    pub id: i64,
    pub secret_answer: String,
}

pub fn parse_AccountDeleteCharacter(payload: &str) -> Result<AccountDeleteCharacter, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let secret_answer = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountDeleteCharacter {
        id,
        secret_answer,    };
    
    Ok(result)
}
