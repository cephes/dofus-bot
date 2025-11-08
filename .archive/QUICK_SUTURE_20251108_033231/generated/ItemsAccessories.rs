//! Generated parser for ItemsAccessories
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ItemsAccessories {
    /// Dofus ID
    pub id: i64,
    /// Unknown type typ
    pub accessories: String,
}

pub fn parse_ItemsAccessories(payload: &str) -> Result<ItemsAccessories, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let accessories = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ItemsAccessories {
id: id,
        accessories,, ..Default::default()};
    
    Ok(result)
}

