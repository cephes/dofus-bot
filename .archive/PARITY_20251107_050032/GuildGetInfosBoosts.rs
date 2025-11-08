//! Generated parser for GuildGetInfosBoosts
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildGetInfosBoosts {

}

pub fn parse_GuildGetInfosBoosts(payload: &str) -> Result<GuildGetInfosBoosts, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildGetInfosBoosts {
    };
    
    Ok(result)
}
