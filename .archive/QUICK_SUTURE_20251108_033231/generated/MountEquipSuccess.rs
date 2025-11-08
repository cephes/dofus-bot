//! Generated parser for MountEquipSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct MountEquipSuccess {
    /// Unknown type typ
    pub data: String,
}

pub fn parse_MountEquipSuccess(payload: &str) -> Result<MountEquipSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let data = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = MountEquipSuccess {
        data,, ..Default::default()};
    
    Ok(result)
}

