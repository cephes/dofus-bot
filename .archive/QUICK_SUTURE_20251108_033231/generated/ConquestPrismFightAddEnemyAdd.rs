//! Generated parser for ConquestPrismFightAddEnemyAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ConquestPrismFightAddEnemyAdd {

}

pub fn parse_ConquestPrismFightAddEnemyAdd(payload: &str) -> Result<ConquestPrismFightAddEnemyAdd, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = ConquestPrismFightAddEnemyAdd {, ..Default::default()};
    
    Ok(result)
}

