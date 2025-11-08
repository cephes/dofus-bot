//! Generated parser for ChatServerMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ChatServerMessage {
    /// Text message
    pub message: String,
}

pub fn parse_ChatServerMessage(payload: &str) -> Result<ChatServerMessage, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let message = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ChatServerMessage {
        message,  ..Default::default()};
    
    Ok(result)
}

