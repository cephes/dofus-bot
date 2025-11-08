//! Generated parser for AccountTicketResponseError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountTicketResponseError {

}

pub fn parse_AccountTicketResponseError(payload: &str) -> Result<AccountTicketResponseError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = AccountTicketResponseError {
    };
    
    Ok(result)
}
