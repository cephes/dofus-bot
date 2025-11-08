//! Generated parser for FriendsNotifyChange
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct FriendsNotifyChange {
    pub notify: bool,
}

pub fn parse_FriendsNotifyChange(payload: &str) -> Result<FriendsNotifyChange, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let notify = common_decode::parse_bool(fields.get(i).unwrap_or(&"false"));
    
    // Create struct instance
    let result = FriendsNotifyChange {
        notify,    };
    
    Ok(result)
}

