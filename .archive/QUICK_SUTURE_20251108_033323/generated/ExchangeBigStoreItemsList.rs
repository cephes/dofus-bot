//! Generated parser for ExchangeBigStoreItemsList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangeBigStoreItemsList {
    /// Dofus ID
    pub template_id: i64,
    /// CSV list (JSON encoded)
    pub items: Vec<typ>,
}

pub fn parse_ExchangeBigStoreItemsList(payload: &str) -> Result<ExchangeBigStoreItemsList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let template_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let items = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ExchangeBigStoreItemsList {
template_id: template_id,
        items,  ..Default::default()};
    
    Ok(result)
}

