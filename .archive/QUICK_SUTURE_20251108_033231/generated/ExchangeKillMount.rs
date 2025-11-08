//! Generated parser for ExchangeKillMount
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeKillMount {

}

pub fn parse_ExchangeKillMount(payload: &str) -> Result<ExchangeKillMount, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeKillMount {, ..Default::default()};
    
    Ok(result)
}

