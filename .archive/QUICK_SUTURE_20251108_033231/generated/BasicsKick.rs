//! Generated parser for BasicsKick
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BasicsKick {

}

pub fn parse_BasicsKick(payload: &str) -> Result<BasicsKick, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = BasicsKick {, ..Default::default()};
    
    Ok(result)
}

