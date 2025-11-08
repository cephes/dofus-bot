//! Generated parser for ChatRequestSubscribeChannelRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ChatRequestSubscribeChannelRemove {
    /// CSV list (JSON encoded)
    pub channels: Vec<String>,
}

pub fn parse_ChatRequestSubscribeChannelRemove(payload: &str) -> Result<ChatRequestSubscribeChannelRemove, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let channels = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ChatRequestSubscribeChannelRemove {
        channels,    };
    
    Ok(result)
}
