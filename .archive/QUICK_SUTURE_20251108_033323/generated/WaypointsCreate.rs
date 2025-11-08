//! Generated parser for WaypointsCreate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct WaypointsCreate {

}

pub fn parse_WaypointsCreate(payload: &str) -> Result<WaypointsCreate, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = WaypointsCreate { ..Default::default() };
    
    Ok(result)
}

