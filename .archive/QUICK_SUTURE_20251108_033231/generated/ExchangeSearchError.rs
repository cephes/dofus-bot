//! Generated parser for ExchangeSearchError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeSearchError {

}

pub fn parse_ExchangeSearchError(payload: &str) -> Result<ExchangeSearchError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeSearchError {, ..Default::default()};
    
    Ok(result)
}

