//! Generated parser for AccountGetGifts
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountGetGifts {
    pub lang: String,
}

pub fn parse_AccountGetGifts(payload: &str) -> Result<AccountGetGifts, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let lang = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountGetGifts {
        lang,  ..Default::default()};
    
    Ok(result)
}

