//! Generated parser for ItemsQuantity
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ItemsQuantity {
    /// Dofus ID
    pub id: i64,
    pub quantity: i64,
}

pub fn parse_ItemsQuantity(payload: &str) -> Result<ItemsQuantity, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let quantity = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ItemsQuantity {
        id,
        quantity,    };
    
    Ok(result)
}


