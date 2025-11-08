//! Generated parser for TutorialCreate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct TutorialCreate {

}

pub fn parse_TutorialCreate(payload: &str) -> Result<TutorialCreate, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = TutorialCreate {
    };
    
    Ok(result)
}
