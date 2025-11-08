//! Generated parser for ChatSend
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ChatSend {
    /// Unknown type dofustyp
    pub chat_channel: String,
    pub private_receiver: String,
    /// Text message
    pub message: String,
    pub params: String,
}

pub fn parse_ChatSend(payload: &str) -> Result<ChatSend, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let chat_channel = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let private_receiver = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let message = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let params = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ChatSend {
        chat_channel,
        private_receiver,
        message,
        params,    };
    
    Ok(result)
}
