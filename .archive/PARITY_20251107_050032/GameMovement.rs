//! Generated parser for GameMovement
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameMovement {
    /// CSV list (JSON encoded)
    pub sprites: Vec<String>,
}

pub fn parse_GameMovement(payload: &str) -> Result<GameMovement, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let sprites = common_decode::parse_string_list(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = GameMovement {
        sprites,    };
    
    Ok(result)
}
