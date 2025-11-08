//! Generated parser for QuestGetList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct QuestGetList {

}

pub fn parse_QuestGetList(payload: &str) -> Result<QuestGetList, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = QuestGetList {
    };
    
    Ok(result)
}
