//! Generated parser for GuildCreateSuccess
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GuildCreateSuccess {

}

pub fn parse_GuildCreateSuccess(payload: &str) -> Result<GuildCreateSuccess, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildCreateSuccess {, ..Default::default()};
    
    Ok(result)
}

