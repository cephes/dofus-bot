//! Generated parser for ExchangeBigStoreItemList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeBigStoreItemList {
    /// Dofus ID
    pub item_template_id: i64,
}

pub fn parse_ExchangeBigStoreItemList(payload: &str) -> Result<ExchangeBigStoreItemList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_template_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangeBigStoreItemList {
        item_template_id,  ..Default::default()};
    
    Ok(result)
}

