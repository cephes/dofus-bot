//! Generated parser for BasicsSubscriberRestrictionRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct BasicsSubscriberRestrictionRemove {

}

pub fn parse_BasicsSubscriberRestrictionRemove(payload: &str) -> Result<BasicsSubscriberRestrictionRemove, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = BasicsSubscriberRestrictionRemove {, ..Default::default()};
    
    Ok(result)
}

