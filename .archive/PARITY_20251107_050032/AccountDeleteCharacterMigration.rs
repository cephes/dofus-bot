//! Generated parser for AccountDeleteCharacterMigration
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountDeleteCharacterMigration {

}

pub fn parse_AccountDeleteCharacterMigration(payload: &str) -> Result<AccountDeleteCharacterMigration, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = AccountDeleteCharacterMigration {
    };
    
    Ok(result)
}
