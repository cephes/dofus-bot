//! Generated parser for SpellsUpgradeSpellSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct SpellsUpgradeSpellSuccess {
    /// Dofus ID
    pub id: i64,
    /// Level
    pub level: i32,
}

pub fn parse_SpellsUpgradeSpellSuccess(payload: &str) -> Result<SpellsUpgradeSpellSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let level = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = SpellsUpgradeSpellSuccess {
        id,
        level,    };
    
    Ok(result)
}
