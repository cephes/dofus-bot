//! Generated parser for ExchangeRequestAskOfflineExchange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeRequestAskOfflineExchange {

}

pub fn parse_ExchangeRequestAskOfflineExchange(payload: &str) -> Result<ExchangeRequestAskOfflineExchange, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeRequestAskOfflineExchange {, ..Default::default()};
    
    Ok(result)
}

