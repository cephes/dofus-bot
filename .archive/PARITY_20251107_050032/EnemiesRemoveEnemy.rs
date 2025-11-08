//! Generated parser for EnemiesRemoveEnemy
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EnemiesRemoveEnemy {

}

pub fn parse_EnemiesRemoveEnemy(payload: &str) -> Result<EnemiesRemoveEnemy, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EnemiesRemoveEnemy {
    };
    
    Ok(result)
}
