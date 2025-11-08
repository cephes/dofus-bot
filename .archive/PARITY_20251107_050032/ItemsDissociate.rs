//! Generated parser for ItemsDissociate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ItemsDissociate {

}

pub fn parse_ItemsDissociate(payload: &str) -> Result<ItemsDissociate, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ItemsDissociate {
    };
    
    Ok(result)
}
