//! Generated parser for PartyFollowError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct PartyFollowError {

}

pub fn parse_PartyFollowError(payload: &str) -> Result<PartyFollowError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyFollowError {
    };
    
    Ok(result)
}
