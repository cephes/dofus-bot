//! Generated parser for ChatSubscribeChannelRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ChatSubscribeChannelRemove {
    /// CSV list (JSON encoded)
    pub channels: Vec<rune>,
}

pub fn parse_ChatSubscribeChannelRemove(payload: &str) -> Result<ChatSubscribeChannelRemove, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let channels = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ChatSubscribeChannelRemove {
        channels,, ..Default::default()};
    
    Ok(result)
}

