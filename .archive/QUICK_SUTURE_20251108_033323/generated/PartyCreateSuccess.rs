//! Generated parser for PartyCreateSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PartyCreateSuccess {

}

pub fn parse_PartyCreateSuccess(payload: &str) -> Result<PartyCreateSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyCreateSuccess { ..Default::default() };
    
    Ok(result)
}

