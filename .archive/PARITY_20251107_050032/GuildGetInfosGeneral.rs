//! Generated parser for GuildGetInfosGeneral
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildGetInfosGeneral {

}

pub fn parse_GuildGetInfosGeneral(payload: &str) -> Result<GuildGetInfosGeneral, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildGetInfosGeneral {
    };
    
    Ok(result)
}
