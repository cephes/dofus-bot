//! Generated parser for GuildInfosHouses
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildInfosHouses {

}

pub fn parse_GuildInfosHouses(payload: &str) -> Result<GuildInfosHouses, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildInfosHouses {
    };
    
    Ok(result)
}
