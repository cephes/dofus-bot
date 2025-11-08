//! Generated parser for InfosMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct InfosMessage {
    /// Dofus ID
    pub chat_id: i64,
    /// CSV list (JSON encoded)
    pub messages: Vec<String>,
}

pub fn parse_InfosMessage(payload: &str) -> Result<InfosMessage, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let chat_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let messages = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = InfosMessage {
        chat_id,
        messages,    };
    
    Ok(result)
}
