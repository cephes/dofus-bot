//! Generated parser for PartyRefuse
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct PartyRefuse {

}

pub fn parse_PartyRefuse(payload: &str) -> Result<PartyRefuse, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = PartyRefuse {
    };
    
    Ok(result)
}
