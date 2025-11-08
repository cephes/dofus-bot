//! Generated parser for ExchangeRequestSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeRequestSuccess {

}

pub fn parse_ExchangeRequestSuccess(payload: &str) -> Result<ExchangeRequestSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeRequestSuccess {, ..Default::default()};
    
    Ok(result)
}

