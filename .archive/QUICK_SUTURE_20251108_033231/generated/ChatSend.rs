//! Generated parser for ChatSend
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ChatSend {
    /// Unknown type dofustyp
    pub chat_channel: String,
    pub private_receiver: String,
    /// Text message
    pub message: String,
    pub params: String,
}

pub fn parse_ChatSend(payload: &str) -> Result<ChatSend, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let chat_channel = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let private_receiver = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let message = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let params = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ChatSend {
chat_channel: chat_channel,
private_receiver: private_receiver,
message: message,
        params,, ..Default::default()};
    
    Ok(result)
}

