//! Generated parser for ItemsWeight
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsWeight {
    pub current: i64,
    pub max: i64,
}

pub fn parse_ItemsWeight(payload: &str) -> Result<ItemsWeight, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let current = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let max = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ItemsWeight {
        current,
        max,    };
    
    Ok(result)
}
