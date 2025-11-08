//! Generated parser for DialogLeave
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct DialogLeave {

}

pub fn parse_DialogLeave(payload: &str) -> Result<DialogLeave, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = DialogLeave {
    };
    
    Ok(result)
}
