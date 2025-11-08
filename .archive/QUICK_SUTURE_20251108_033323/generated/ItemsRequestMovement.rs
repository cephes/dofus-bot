//! Generated parser for ItemsRequestMovement
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ItemsRequestMovement {
    /// Dofus ID
    pub id: i64,
    /// Position list
    pub position: Vec<i64>,
    pub quantity: i64,
}

pub fn parse_ItemsRequestMovement(payload: &str) -> Result<ItemsRequestMovement, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let position = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
        let quantity = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ItemsRequestMovement {
id: id,
position: position,
        quantity,  ..Default::default()};
    
    Ok(result)
}

