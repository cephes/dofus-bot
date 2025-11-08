//! Generated parser for ItemsItemSetAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ItemsItemSetAdd {
    /// Dofus ID
    pub id: i64,
    /// CSV list of integers
    pub items_templates_ids: Vec<i64>,
    /// CSV list (JSON encoded)
    pub effects: Vec<retrotyp>,
}

pub fn parse_ItemsItemSetAdd(payload: &str) -> Result<ItemsItemSetAdd, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let items_templates_ids = common_decode::parse_i64_list(fields.get(i).unwrap_or(&""));
        let effects = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = ItemsItemSetAdd {
        id,
        items_templates_ids,
        effects,    };
    
    Ok(result)
}


