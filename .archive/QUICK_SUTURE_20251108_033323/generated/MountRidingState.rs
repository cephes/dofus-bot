//! Generated parser for MountRidingState
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct MountRidingState {
    /// Dofus ID
    pub riding: i64,
}

pub fn parse_MountRidingState(payload: &str) -> Result<MountRidingState, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let riding = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = MountRidingState {
        riding,  ..Default::default()};
    
    Ok(result)
}

