//! Generated parser for ExchangePutInMountParkFromShed
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ExchangePutInMountParkFromShed {
    /// Dofus ID
    pub mount_id: i64,
}

pub fn parse_ExchangePutInMountParkFromShed(payload: &str) -> Result<ExchangePutInMountParkFromShed, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let mount_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangePutInMountParkFromShed {
        mount_id,  ..Default::default()};
    
    Ok(result)
}

