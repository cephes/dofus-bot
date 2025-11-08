//! Generated parser for AccountCharacterMigrationSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountCharacterMigrationSuccess {

}

pub fn parse_AccountCharacterMigrationSuccess(payload: &str) -> Result<AccountCharacterMigrationSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = AccountCharacterMigrationSuccess {, ..Default::default()};
    
    Ok(result)
}

