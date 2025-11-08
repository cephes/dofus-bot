//! Generated parser for FightsBlockJoinerExceptParty
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct FightsBlockJoinerExceptParty {

}

pub fn parse_FightsBlockJoinerExceptParty(payload: &str) -> Result<FightsBlockJoinerExceptParty, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = FightsBlockJoinerExceptParty {
    };
    
    Ok(result)
}
