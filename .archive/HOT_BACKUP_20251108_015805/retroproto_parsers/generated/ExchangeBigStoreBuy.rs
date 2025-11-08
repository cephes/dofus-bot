//! Generated parser for ExchangeBigStoreBuy
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ExchangeBigStoreBuy {
    /// Dofus ID
    pub item_id: i64,
    pub quantity_index: i64,
    pub price: i64,
}

pub fn parse_ExchangeBigStoreBuy(payload: &str) -> Result<ExchangeBigStoreBuy, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let quantity_index = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let price = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangeBigStoreBuy {
        item_id,
        quantity_index,
        price,    };
    
    Ok(result)
}

