//! Generated parser for WaypointsCreate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct WaypointsCreate {

}

pub fn parse_WaypointsCreate(payload: &str) -> Result<WaypointsCreate, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = WaypointsCreate {
    };
    
    Ok(result)
}
