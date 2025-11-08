//! Generated parser for GildHireTaxCollectorSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GildHireTaxCollectorSuccess {

}

pub fn parse_GildHireTaxCollectorSuccess(payload: &str) -> Result<GildHireTaxCollectorSuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GildHireTaxCollectorSuccess {
    };
    
    Ok(result)
}
