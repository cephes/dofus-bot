//! Generated parser for BasicsSubscriberRestrictionAdd
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BasicsSubscriberRestrictionAdd {
    /// Dofus ID
    pub dialog_id: i64,
}

pub fn parse_BasicsSubscriberRestrictionAdd(payload: &str) -> Result<BasicsSubscriberRestrictionAdd, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let dialog_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = BasicsSubscriberRestrictionAdd {
        dialog_id,, ..Default::default()};
    
    Ok(result)
}

