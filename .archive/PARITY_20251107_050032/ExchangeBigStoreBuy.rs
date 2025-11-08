//! Generated parser for ExchangeBigStoreBuy
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreBuy {
    /// Dofus ID
    pub item_id: i64,
    pub quantity_index: i64,
    pub price: i64,
}

pub fn parse_ExchangeBigStoreBuy(payload: &str) -> Result<ExchangeBigStoreBuy, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let quantity_index = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let price = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeBigStoreBuy {
        item_id,
        quantity_index,
        price,    };
    
    Ok(result)
}
