//! Generated parser for AccountCharacterSelectedSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
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
    pub items: Vec<String>,
}

pub fn parse_AccountCharacterSelectedSuccess(payload: &str) -> Result<AccountCharacterSelectedSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let name = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let level = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let class_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let sex = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let gfx_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let color1 = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let color2 = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let color3 = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let items = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountCharacterSelectedSuccess {
        id,
        name,
        level,
        class_id,
        sex,
        gfx_id,
        color1,
        color2,
        color3,
        items,    };
    
    Ok(result)
}
