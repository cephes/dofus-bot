//! Generated parser for PartyRequestFollow
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PartyRequestFollow {

}

pub fn parse_PartyRequestFollow(payload: &str) -> Result<PartyRequestFollow, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyRequestFollow {, ..Default::default()};
    
    Ok(result)
}

