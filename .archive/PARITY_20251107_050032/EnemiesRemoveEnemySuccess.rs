//! Generated parser for EnemiesRemoveEnemySuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct EnemiesRemoveEnemySuccess {

}

pub fn parse_EnemiesRemoveEnemySuccess(payload: &str) -> Result<EnemiesRemoveEnemySuccess, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EnemiesRemoveEnemySuccess {
    };
    
    Ok(result)
}
