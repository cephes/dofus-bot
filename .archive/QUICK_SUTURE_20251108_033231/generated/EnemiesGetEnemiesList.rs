//! Generated parser for EnemiesGetEnemiesList
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct EnemiesGetEnemiesList {

}

pub fn parse_EnemiesGetEnemiesList(payload: &str) -> Result<EnemiesGetEnemiesList, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = EnemiesGetEnemiesList {, ..Default::default()};
    
    Ok(result)
}

