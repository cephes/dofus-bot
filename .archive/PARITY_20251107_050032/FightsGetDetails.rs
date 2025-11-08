//! Generated parser for FightsGetDetails
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct FightsGetDetails {

}

pub fn parse_FightsGetDetails(payload: &str) -> Result<FightsGetDetails, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = FightsGetDetails {
    };
    
    Ok(result)
}
