//! Generated parser for SpellsUpgradeSpellSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct SpellsUpgradeSpellSuccess {
    /// Dofus ID
    pub id: i64,
    /// Level
    pub level: i32,
}

pub fn parse_SpellsUpgradeSpellSuccess(payload: &str) -> Result<SpellsUpgradeSpellSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let level = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = SpellsUpgradeSpellSuccess {
id: id,
        level,, ..Default::default()};
    
    Ok(result)
}

