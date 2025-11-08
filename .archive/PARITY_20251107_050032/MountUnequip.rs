//! Generated parser for MountUnequip
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct MountUnequip {

}

pub fn parse_MountUnequip(payload: &str) -> Result<MountUnequip, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = MountUnequip {
    };
    
    Ok(result)
}
