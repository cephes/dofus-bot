//! Generated parser for SpellsChangeOption
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct SpellsChangeOption {
    pub can_use_see_all_spell: bool,
}

pub fn parse_SpellsChangeOption(payload: &str) -> Result<SpellsChangeOption, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let can_use_see_all_spell = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
    
    // Create struct instance
    let result = SpellsChangeOption {
        can_use_see_all_spell,    };
    
    Ok(result)
}
