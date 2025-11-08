//! Generated parser for GuildRemoveTaxCollector
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildRemoveTaxCollector {

}

pub fn parse_GuildRemoveTaxCollector(payload: &str) -> Result<GuildRemoveTaxCollector, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildRemoveTaxCollector {
    };
    
    Ok(result)
}
