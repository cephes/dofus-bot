//! Generated parser for ChatReportMessage
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ChatReportMessage {

}

pub fn parse_ChatReportMessage(payload: &str) -> Result<ChatReportMessage, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ChatReportMessage {, ..Default::default()};
    
    Ok(result)
}

