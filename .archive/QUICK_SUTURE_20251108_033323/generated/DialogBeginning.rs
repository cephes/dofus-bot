//! Generated parser for DialogBeginning
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct DialogBeginning {
    /// Dofus ID
    pub npc_id: i64,
}

pub fn parse_DialogBeginning(payload: &str) -> Result<DialogBeginning, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let npc_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = DialogBeginning {
        npc_id,  ..Default::default()};
    
    Ok(result)
}

