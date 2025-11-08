//! Generated parser for ConquestPrismFightAddEnemyRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ConquestPrismFightAddEnemyRemove {

}

pub fn parse_ConquestPrismFightAddEnemyRemove(payload: &str) -> Result<ConquestPrismFightAddEnemyRemove, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ConquestPrismFightAddEnemyRemove {
    };
    
    Ok(result)
}
