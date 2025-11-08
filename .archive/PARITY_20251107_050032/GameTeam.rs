//! Generated parser for GameTeam
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameTeam {

}

pub fn parse_GameTeam(payload: &str) -> Result<GameTeam, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GameTeam {
    };
    
    Ok(result)
}
