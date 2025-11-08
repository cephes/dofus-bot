//! Generated parser for GuildInfosTaxCollectorsAttackers
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct GuildInfosTaxCollectorsAttackers {

}

pub fn parse_GuildInfosTaxCollectorsAttackers(payload: &str) -> Result<GuildInfosTaxCollectorsAttackers, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = GuildInfosTaxCollectorsAttackers { ..Default::default() };
    
    Ok(result)
}

