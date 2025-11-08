//! Generated parser for MountEquipSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
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
        data,    };
    
    Ok(result)
}

