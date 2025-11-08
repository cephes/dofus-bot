//! Generated parser for PartyFollowAll
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PartyFollowAll {

}

pub fn parse_PartyFollowAll(payload: &str) -> Result<PartyFollowAll, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyFollowAll { ..Default::default() };
    
    Ok(result)
}

