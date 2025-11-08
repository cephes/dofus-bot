//! Generated parser for ExchangePayMovementSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangePayMovementSuccess {

}

pub fn parse_ExchangePayMovementSuccess(payload: &str) -> Result<ExchangePayMovementSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangePayMovementSuccess { ..Default::default() };
    
    Ok(result)
}

