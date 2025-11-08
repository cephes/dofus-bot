//! Generated parser for ItemsItemFound
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsItemFound {

}

pub fn parse_ItemsItemFound(payload: &str) -> Result<ItemsItemFound, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ItemsItemFound {
    };
    
    Ok(result)
}
