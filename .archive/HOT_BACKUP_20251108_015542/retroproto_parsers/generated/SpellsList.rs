//! Generated parser for SpellsList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct SpellsList {
    /// CSV list (JSON encoded)
    pub spells: Vec<retro>,
}

pub fn parse_SpellsList(payload: &str) -> Result<SpellsList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let spells = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = SpellsList {
        spells,    };
    
    Ok(result)
}

