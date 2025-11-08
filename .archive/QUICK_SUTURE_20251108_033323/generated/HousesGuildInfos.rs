//! Generated parser for HousesGuildInfos
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct HousesGuildInfos {

}

pub fn parse_HousesGuildInfos(payload: &str) -> Result<HousesGuildInfos, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = HousesGuildInfos { ..Default::default() };
    
    Ok(result)
}

