//! Generated parser for GameActionCancel
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameActionCancel {
    /// Dofus ID
    pub id: i64,
    pub params: String,
}

pub fn parse_GameActionCancel(payload: &str) -> Result<GameActionCancel, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let params = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = GameActionCancel {
id: id,
        params,, ..Default::default()};
    
    Ok(result)
}

