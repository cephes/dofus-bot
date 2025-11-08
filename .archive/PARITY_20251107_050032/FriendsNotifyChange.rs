//! Generated parser for FriendsNotifyChange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct FriendsNotifyChange {
    pub notify: bool,
}

pub fn parse_FriendsNotifyChange(payload: &str) -> Result<FriendsNotifyChange, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let notify = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
    
    // Create struct instance
    let result = FriendsNotifyChange {
        notify,    };
    
    Ok(result)
}
