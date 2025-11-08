//! Generated parser for ExchangeBigStoreItemsList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreItemsList {
    /// Dofus ID
    pub template_id: i64,
    /// CSV list (JSON encoded)
    pub items: Vec<String>,
}

pub fn parse_ExchangeBigStoreItemsList(payload: &str) -> Result<ExchangeBigStoreItemsList, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let template_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let items = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = ExchangeBigStoreItemsList {
        template_id,
        items,    };
    
    Ok(result)
}
