//! Generated parser for MountXP
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct MountXP {
    /// Percentage (0.0-1.0)
    pub percent: f64,
}

pub fn parse_MountXP(payload: &str) -> Result<MountXP, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let percent = common_decode::parse_f64(fields.get(i).unwrap_or(&"0.0"));
    
    // Create struct instance
    let result = MountXP {
        percent,  ..Default::default()};
    
    Ok(result)
}

