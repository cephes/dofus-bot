//! Generated parser for GuildAcceptInvitation
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GuildAcceptInvitation {

}

pub fn parse_GuildAcceptInvitation(payload: &str) -> Result<GuildAcceptInvitation, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildAcceptInvitation {
    };
    
    Ok(result)
}
