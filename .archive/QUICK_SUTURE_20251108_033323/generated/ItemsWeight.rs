//! Generated parser for ItemsWeight
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ItemsWeight {
    pub current: i64,
    pub max: i64,
}

pub fn parse_ItemsWeight(payload: &str) -> Result<ItemsWeight, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let current = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let max = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ItemsWeight {
current: current,
        max,  ..Default::default()};
    
    Ok(result)
}

