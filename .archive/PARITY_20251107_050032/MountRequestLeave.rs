//! Generated parser for MountRequestLeave
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct MountRequestLeave {

}

pub fn parse_MountRequestLeave(payload: &str) -> Result<MountRequestLeave, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = MountRequestLeave {
    };
    
    Ok(result)
}
