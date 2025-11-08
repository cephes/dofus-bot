//! Generated parser for ExchangeBigStoreTypeItemsList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ExchangeBigStoreTypeItemsList {
    /// Unknown type retrotyp
    pub item_type: String,
    /// CSV list of integers
    pub item_template_ids: Vec<i64>,
}

pub fn parse_ExchangeBigStoreTypeItemsList(payload: &str) -> Result<ExchangeBigStoreTypeItemsList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_type = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let item_template_ids = common_decode::parse_i64_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ExchangeBigStoreTypeItemsList {
        item_type,
        item_template_ids,    };
    
    Ok(result)
}


