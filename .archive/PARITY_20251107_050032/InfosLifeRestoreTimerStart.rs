//! Generated parser for InfosLifeRestoreTimerStart
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct InfosLifeRestoreTimerStart {
    /// Unknown type time
    pub interval: String,
}

pub fn parse_InfosLifeRestoreTimerStart(payload: &str) -> Result<InfosLifeRestoreTimerStart, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let interval = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = InfosLifeRestoreTimerStart {
        interval,    };
    
    Ok(result)
}
