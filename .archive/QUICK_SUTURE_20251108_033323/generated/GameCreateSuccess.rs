//! Generated parser for GameCreateSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GameCreateSuccess {
    pub r#type: i64,
}

pub fn parse_GameCreateSuccess(payload: &str) -> Result<GameCreateSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let r#type = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = GameCreateSuccess {
        r#type: r#type,  ..Default::default()};
    
    Ok(result)
}

