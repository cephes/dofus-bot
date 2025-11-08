//! Generated parser for ExchangeLeaveError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeLeaveError {

}

pub fn parse_ExchangeLeaveError(payload: &str) -> Result<ExchangeLeaveError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLeaveError {, ..Default::default()};
    
    Ok(result)
}

