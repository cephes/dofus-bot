//! Generated parser for ItemsAddSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ItemsAddSuccess {
    /// CSV list (JSON encoded)
    pub items: Vec<ItemsAddSuccessItem>,
}

pub fn parse_ItemsAddSuccess(payload: &str) -> Result<ItemsAddSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let items = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ItemsAddSuccess {
        items,    };
    
    Ok(result)
}

