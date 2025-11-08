//! Generated parser for ExchangeCreateSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ExchangeCreateSuccess {
    /// Unknown type retrotyp
    pub r#r#type: String,
    /// Unknown type ExchangeCreateSuccessNPCBuy
    pub npc_buy: String,
    /// Unknown type ExchangeCreateSuccessPaddock
    pub paddock: String,
}

pub fn parse_ExchangeCreateSuccess(payload: &str) -> Result<ExchangeCreateSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let r#type = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let npc_buy = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let paddock = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ExchangeCreateSuccess {
        r#r#type,
        npc_buy,
        paddock,    };
    
    Ok(result)
}


