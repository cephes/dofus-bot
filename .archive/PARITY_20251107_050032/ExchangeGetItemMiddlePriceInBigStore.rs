//! Generated parser for ExchangeGetItemMiddlePriceInBigStore
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeGetItemMiddlePriceInBigStore {
    /// Dofus ID
    pub template_id: i64,
}

pub fn parse_ExchangeGetItemMiddlePriceInBigStore(payload: &str) -> Result<ExchangeGetItemMiddlePriceInBigStore, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let template_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeGetItemMiddlePriceInBigStore {
        template_id,    };
    
    Ok(result)
}
