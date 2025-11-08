//! Generated parser for MountRequestData
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct MountRequestData {
    /// Dofus ID
    pub id: i64,
    /// Dofus ID
    pub validity: i64,
}

pub fn parse_MountRequestData(payload: &str) -> Result<MountRequestData, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let validity = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = MountRequestData {
id: id,
        validity,, ..Default::default()};
    
    Ok(result)
}

