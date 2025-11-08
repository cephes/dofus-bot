//! Generated parser for ConquestGetAlignedBonus
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ConquestGetAlignedBonus {

}

pub fn parse_ConquestGetAlignedBonus(payload: &str) -> Result<ConquestGetAlignedBonus, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ConquestGetAlignedBonus { ..Default::default() };
    
    Ok(result)
}

