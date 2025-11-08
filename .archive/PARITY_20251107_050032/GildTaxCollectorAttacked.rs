//! Generated parser for GildTaxCollectorAttacked
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GildTaxCollectorAttacked {

}

pub fn parse_GildTaxCollectorAttacked(payload: &str) -> Result<GildTaxCollectorAttacked, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GildTaxCollectorAttacked {
    };
    
    Ok(result)
}
