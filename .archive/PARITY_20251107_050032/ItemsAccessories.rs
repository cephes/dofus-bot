//! Generated parser for ItemsAccessories
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsAccessories {
    /// Dofus ID
    pub id: i64,
    /// Unknown type typ
    pub accessories: String,
}

pub fn parse_ItemsAccessories(payload: &str) -> Result<ItemsAccessories, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let accessories = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ItemsAccessories {
        id,
        accessories,    };
    
    Ok(result)
}
