//! Generated parser for InfosLifeRestoreTimerFinish
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct InfosLifeRestoreTimerFinish {
    pub restored: i64,
}

pub fn parse_InfosLifeRestoreTimerFinish(payload: &str) -> Result<InfosLifeRestoreTimerFinish, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let restored = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = InfosLifeRestoreTimerFinish {
        restored,, ..Default::default()};
    
    Ok(result)
}

