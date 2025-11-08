//! Generated parser for ExchangeBigStoreSearch
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeBigStoreSearch {
    /// Unknown type retrotyp
    pub item_r_type: String,
    /// Dofus ID
    pub template_id: i64,
}

pub fn parse_ExchangeBigStoreSearch(payload: &str) -> Result<ExchangeBigStoreSearch, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let item_r_type = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
        let template_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeBigStoreSearch {
        item_r_type,
        template_id,    };
    
    Ok(result)
}
