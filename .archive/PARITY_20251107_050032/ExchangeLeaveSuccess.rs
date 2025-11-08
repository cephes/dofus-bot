//! Generated parser for ExchangeLeaveSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeLeaveSuccess {
    pub player_exchange_type: bool,
}

pub fn parse_ExchangeLeaveSuccess(payload: &str) -> Result<ExchangeLeaveSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let rtype_player_exchange = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = ExchangeLeaveSuccess {
        player_exchange_type: rtype_player_exchange,    };
    
    Ok(result)
}
