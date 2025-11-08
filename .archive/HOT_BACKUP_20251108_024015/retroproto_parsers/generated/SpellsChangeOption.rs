//! Generated parser for SpellsChangeOption
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct SpellsChangeOption {
    pub can_use_see_all_spell: bool,
}

pub fn parse_SpellsChangeOption(payload: &str) -> Result<SpellsChangeOption, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let can_use_see_all_spell = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = SpellsChangeOption {
        can_use_see_all_spell,    };
    
    Ok(result)
}


