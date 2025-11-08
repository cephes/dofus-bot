//! Generated parser for ItemsUseNoConfirm
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsUseNoConfirm {
    /// Dofus ID
    pub id: i64,
    /// Dofus ID
    pub sprite_id: i64,
    /// Map cell number
    pub cell: i32,
}

pub fn parse_ItemsUseNoConfirm(payload: &str) -> Result<ItemsUseNoConfirm, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let sprite_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let cell = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ItemsUseNoConfirm {
        id,
        sprite_id,
        cell,    };
    
    Ok(result)
}
