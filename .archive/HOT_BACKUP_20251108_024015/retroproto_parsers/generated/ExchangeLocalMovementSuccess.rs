//! Generated parser for ExchangeLocalMovementSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ExchangeLocalMovementSuccess {

}

pub fn parse_ExchangeLocalMovementSuccess(payload: &str) -> Result<ExchangeLocalMovementSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeLocalMovementSuccess {
    };
    
    Ok(result)
}


