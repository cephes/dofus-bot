//! Generated parser for ExchangeCraftLoopEnd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeCraftLoopEnd {

}

pub fn parse_ExchangeCraftLoopEnd(payload: &str) -> Result<ExchangeCraftLoopEnd, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ExchangeCraftLoopEnd {
    };
    
    Ok(result)
}
