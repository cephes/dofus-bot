//! Generated parser for BasicsWhoIsError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BasicsWhoIsError {

}

pub fn parse_BasicsWhoIsError(payload: &str) -> Result<BasicsWhoIsError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = BasicsWhoIsError { ..Default::default() };
    
    Ok(result)
}

