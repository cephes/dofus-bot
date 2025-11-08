//! Generated parser for AccountCharacterSelectedSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountCharacterSelectedSuccess {
    /// Dofus ID
    pub id: i64,
    /// Name/label
    pub name: String,
    /// Level
    pub level: i32,
    /// Dofus ID
    pub class_id: i64,
    pub sex: i64,
    /// Dofus ID
    pub gfx_id: i64,
    /// Color value
    pub color1: i32,
    /// Color value
    pub color2: i32,
    /// Color value
    pub color3: i32,
    /// CSV list (JSON encoded)
    pub items: Vec<typ>,
}

pub fn parse_AccountCharacterSelectedSuccess(payload: &str) -> Result<AccountCharacterSelectedSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let name = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let level = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let class_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let sex = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let gfx_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let color1 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let color2 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let color3 = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
        let items = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = AccountCharacterSelectedSuccess {
id: id,
name: name,
level: level,
class_id: class_id,
sex: sex,
gfx_id: gfx_id,
color1: color1,
color2: color2,
color3: color3,
        items,  ..Default::default()};
    
    Ok(result)
}

