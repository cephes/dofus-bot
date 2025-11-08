//! Generated parser for AccountServersListError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountServersListError {

}

pub fn parse_AccountServersListError(payload: &str) -> Result<AccountServersListError, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = AccountServersListError {, ..Default::default()};
    
    Ok(result)
}

