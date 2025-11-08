//! Generated parser for ChatServerMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ChatServerMessage {
    /// Text message
    pub message: String,
}

pub fn parse_ChatServerMessage(payload: &str) -> Result<ChatServerMessage, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let message = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ChatServerMessage {
        message,    };
    
    Ok(result)
}
