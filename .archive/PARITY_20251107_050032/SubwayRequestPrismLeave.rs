//! Generated parser for SubwayRequestPrismLeave
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct SubwayRequestPrismLeave {

}

pub fn parse_SubwayRequestPrismLeave(payload: &str) -> Result<SubwayRequestPrismLeave, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = SubwayRequestPrismLeave {
    };
    
    Ok(result)
}
