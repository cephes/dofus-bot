//! Generated parser for MountXP
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct MountXP {
    /// Percentage (0.0-1.0)
    pub percent: f64,
}

pub fn parse_MountXP(payload: &str) -> Result<MountXP, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let percent = common_decode::parse_f64(_fields.get(i).unwrap_or(&"0.0"));
        i += 1;
    
    // Create struct instance
    let result = MountXP {
        percent,    };
    
    Ok(result)
}
