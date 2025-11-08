//! Generated parser for ExchangeCraftPublicMode
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeCraftPublicMode {

}

pub fn parse_ExchangeCraftPublicMode(payload: &str) -> Result<ExchangeCraftPublicMode, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeCraftPublicMode {
    };
    
    Ok(result)
}
