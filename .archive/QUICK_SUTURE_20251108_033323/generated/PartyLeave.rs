//! Generated parser for PartyLeave
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PartyLeave {

}

pub fn parse_PartyLeave(payload: &str) -> Result<PartyLeave, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyLeave { ..Default::default() };
    
    Ok(result)
}

