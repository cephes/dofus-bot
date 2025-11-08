//! Generated parser for ItemsTool
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ItemsTool {
    /// Dofus ID
    pub job_id: i64,
}

pub fn parse_ItemsTool(payload: &str) -> Result<ItemsTool, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let job_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ItemsTool {
        job_id,, ..Default::default()};
    
    Ok(result)
}

