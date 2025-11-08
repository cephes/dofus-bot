//! Generated parser for ExchangeCreateSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeCreateSuccess {
    /// Unknown type retrotyp
    pub rr_type: String,
    /// Unknown type ExchangeCreateSuccessNPCBuy
    pub npc_buy: String,
    /// Unknown type ExchangeCreateSuccessPaddock
    pub paddock: String,
}

pub fn parse_ExchangeCreateSuccess(payload: &str) -> Result<ExchangeCreateSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let rr_type = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        let npc_buy = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let paddock = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ExchangeCreateSuccess {
        rr_type,
        npc_buy,
        paddock,    };
    
    Ok(result)
}
