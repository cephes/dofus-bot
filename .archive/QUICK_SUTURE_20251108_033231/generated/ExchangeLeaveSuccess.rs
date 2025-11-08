//! Generated parser for ExchangeLeaveSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeLeaveSuccess {
    pub type_player_exchange: bool,
}

pub fn parse_ExchangeLeaveSuccess(payload: &str) -> Result<ExchangeLeaveSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let type_player_exchange = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = ExchangeLeaveSuccess {
        type_player_exchange,, ..Default::default()};
    
    Ok(result)
}

