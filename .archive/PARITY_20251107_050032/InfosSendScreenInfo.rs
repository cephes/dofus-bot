//! Generated parser for InfosSendScreenInfo
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct InfosSendScreenInfo {
    /// Dofus ID
    pub width: i64,
    pub height: i64,
    pub display_state: i64,
}

pub fn parse_InfosSendScreenInfo(payload: &str) -> Result<InfosSendScreenInfo, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let width = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let height = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let display_state = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = InfosSendScreenInfo {
        width,
        height,
        display_state,    };
    
    Ok(result)
}
