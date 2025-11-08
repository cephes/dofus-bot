//! Generated parser for ItemsMovement
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsMovement {
    /// Dofus ID
    pub id: i64,
    /// Position list
    pub position: Vec<i64>,
}

pub fn parse_ItemsMovement(payload: &str) -> Result<ItemsMovement, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let position = common_decode::parse_i64_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ItemsMovement {
        id,
        position,    };
    
    Ok(result)
}
