//! Generated parser for AccountTicketResponseSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountTicketResponseSuccess {
    /// Dofus ID
    pub key_id: i64,
}

pub fn parse_AccountTicketResponseSuccess(payload: &str) -> Result<AccountTicketResponseSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let key_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountTicketResponseSuccess {
        key_id,, ..Default::default()};
    
    Ok(result)
}

