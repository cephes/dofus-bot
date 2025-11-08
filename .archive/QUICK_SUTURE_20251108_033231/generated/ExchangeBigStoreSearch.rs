//! Generated parser for ExchangeBigStoreSearch
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeBigStoreSearch {
    /// Unknown type retrotyp
    pub item_type: String,
    /// Dofus ID
    pub template_id: i64,
}

pub fn parse_ExchangeBigStoreSearch(payload: &str) -> Result<ExchangeBigStoreSearch, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_type = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let template_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangeBigStoreSearch {
item_type: item_type,
        template_id,, ..Default::default()};
    
    Ok(result)
}

