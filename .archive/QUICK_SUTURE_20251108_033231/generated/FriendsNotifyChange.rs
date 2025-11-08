//! Generated parser for FriendsNotifyChange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct FriendsNotifyChange {
    pub notify: bool,
}

pub fn parse_FriendsNotifyChange(payload: &str) -> Result<FriendsNotifyChange, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let notify = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = FriendsNotifyChange {
        notify,, ..Default::default()};
    
    Ok(result)
}

