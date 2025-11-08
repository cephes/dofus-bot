//! Generated parser for EnemiesRemoveEnemyError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EnemiesRemoveEnemyError {

}

pub fn parse_EnemiesRemoveEnemyError(payload: &str) -> Result<EnemiesRemoveEnemyError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EnemiesRemoveEnemyError {
    };
    
    Ok(result)
}
