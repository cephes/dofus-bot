//! Generated parser for AccountTicketResponseSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountTicketResponseSuccess {
    /// Dofus ID
    pub key_id: i64,
}

pub fn parse_AccountTicketResponseSuccess(payload: &str) -> Result<AccountTicketResponseSuccess, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let key_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = AccountTicketResponseSuccess {
        key_id,    };
    
    Ok(result)
}
