//! Generated parser for FightsBlockSpectators
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct FightsBlockSpectators {

}

pub fn parse_FightsBlockSpectators(payload: &str) -> Result<FightsBlockSpectators, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = FightsBlockSpectators {, ..Default::default()};
    
    Ok(result)
}

