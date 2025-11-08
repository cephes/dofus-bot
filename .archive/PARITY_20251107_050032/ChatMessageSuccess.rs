//! Generated parser for ChatMessageSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ChatMessageSuccess {
    /// Unknown type dofustyp
    pub chat_channel: String,
    /// Dofus ID
    pub id: i64,
    pub private_to: bool,
    /// Name/label
    pub name: String,
    /// Text message
    pub message: String,
    pub params: String,
}

pub fn parse_ChatMessageSuccess(payload: &str) -> Result<ChatMessageSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let chat_channel = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let private_to = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
        let name = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let message = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let params = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ChatMessageSuccess {
        chat_channel,
        id,
        private_to,
        name,
        message,
        params,    };
    
    Ok(result)
}
