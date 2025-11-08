//! Generated parser for GameCreate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct GameCreate {
    pub rr_type: i64,
}

pub fn parse_GameCreate(payload: &str) -> Result<GameCreate, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let rr_type = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = GameCreate {
        rr_type,    };
    
    Ok(result)
}
