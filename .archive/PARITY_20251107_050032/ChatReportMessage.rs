//! Generated parser for ChatReportMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ChatReportMessage {

}

pub fn parse_ChatReportMessage(payload: &str) -> Result<ChatReportMessage, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ChatReportMessage {
    };
    
    Ok(result)
}
