//! Generated parser for GameMapData
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct GameMapData {
    /// Dofus ID
    pub id: i64,
    /// Name/label
    pub name: String,
    pub key: String,
}

pub fn parse_GameMapData(payload: &str) -> Result<GameMapData, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let name = common_decode::parse_string(fields.get(i).unwrap_or(&""));
        let key = common_decode::parse_string(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = GameMapData {
        id,
        name,
        key,    };
    
    Ok(result)
}


