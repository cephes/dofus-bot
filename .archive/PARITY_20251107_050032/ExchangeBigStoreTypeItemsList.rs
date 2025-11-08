//! Generated parser for ExchangeBigStoreTypeItemsList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreTypeItemsList {
    /// Unknown type retrotyp
    pub item_r_type: String,
    /// CSV list of integers
    pub item_template_ids: Vec<i64>,
}

pub fn parse_ExchangeBigStoreTypeItemsList(payload: &str) -> Result<ExchangeBigStoreTypeItemsList, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_r_type = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let item_template_ids = common_decode::parse_i64_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ExchangeBigStoreTypeItemsList {
        item_r_type,
        item_template_ids,    };
    
    Ok(result)
}
