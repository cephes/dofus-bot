//! Generated parser for AccountAddCharacter
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct AccountAddCharacter {
    /// Name/label
    pub name: String,
    pub class: i64,
    pub sex: i64,
    /// Color value
    pub color1: i32,
    /// Color value
    pub color2: i32,
    /// Color value
    pub color3: i32,
}

pub fn parse_AccountAddCharacter(payload: &str) -> Result<AccountAddCharacter, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let name = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let class = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let sex = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let color1 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let color2 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let color3 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountAddCharacter {
        name,
        class,
        sex,
        color1,
        color2,
        color3,    };
    
    Ok(result)
}


