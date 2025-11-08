//! Generated parser for FightsBlockJoinerExceptParty
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct FightsBlockJoinerExceptParty {

}

pub fn parse_FightsBlockJoinerExceptParty(payload: &str) -> Result<FightsBlockJoinerExceptParty, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = FightsBlockJoinerExceptParty {
    };
    
    Ok(result)
}

