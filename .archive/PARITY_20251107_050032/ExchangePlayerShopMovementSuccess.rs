//! Generated parser for ExchangePlayerShopMovementSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangePlayerShopMovementSuccess {

}

pub fn parse_ExchangePlayerShopMovementSuccess(payload: &str) -> Result<ExchangePlayerShopMovementSuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangePlayerShopMovementSuccess {
    };
    
    Ok(result)
}
