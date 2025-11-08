//! Generated parser for GameCreate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct GameCreate {
    pub r#type: i64,
}

pub fn parse_GameCreate(payload: &str) -> Result<GameCreate, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let r#type = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = GameCreate {
        r#type,    };
    
    Ok(result)
}

