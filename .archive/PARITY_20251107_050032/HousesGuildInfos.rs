//! Generated parser for HousesGuildInfos
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct HousesGuildInfos {

}

pub fn parse_HousesGuildInfos(payload: &str) -> Result<HousesGuildInfos, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = HousesGuildInfos {
    };
    
    Ok(result)
}
