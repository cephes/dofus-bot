//! Generated parser for ExchangeMovementPay
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeMovementPay {

}

pub fn parse_ExchangeMovementPay(payload: &str) -> Result<ExchangeMovementPay, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeMovementPay {, ..Default::default()};
    
    Ok(result)
}

