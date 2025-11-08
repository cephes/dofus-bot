//! Generated parser for FightsNeedHelp
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct FightsNeedHelp {

}

pub fn parse_FightsNeedHelp(payload: &str) -> Result<FightsNeedHelp, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = FightsNeedHelp {
    };
    
    Ok(result)
}
