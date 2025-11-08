//! Generated parser for ExchangeBigStoreItemsMovementAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreItemsMovementAdd {

}

pub fn parse_ExchangeBigStoreItemsMovementAdd(payload: &str) -> Result<ExchangeBigStoreItemsMovementAdd, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeBigStoreItemsMovementAdd {
    };
    
    Ok(result)
}
