//! Generated parser for InfosMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct InfosMessage {
    /// Dofus ID
    pub chat_id: i64,
    /// CSV list (JSON encoded)
    pub messages: Vec<typ>,
}

pub fn parse_InfosMessage(payload: &str) -> Result<InfosMessage, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let chat_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let messages = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = InfosMessage {
chat_id: chat_id,
        messages,, ..Default::default()};
    
    Ok(result)
}

