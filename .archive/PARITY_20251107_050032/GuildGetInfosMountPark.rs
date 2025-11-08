//! Generated parser for GuildGetInfosMountPark
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildGetInfosMountPark {

}

pub fn parse_GuildGetInfosMountPark(payload: &str) -> Result<GuildGetInfosMountPark, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildGetInfosMountPark {
    };
    
    Ok(result)
}
