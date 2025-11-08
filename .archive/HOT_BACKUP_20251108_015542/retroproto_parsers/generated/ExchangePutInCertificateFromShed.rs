//! Generated parser for ExchangePutInCertificateFromShed
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct ExchangePutInCertificateFromShed {
    /// Dofus ID
    pub mount_id: i64,
}

pub fn parse_ExchangePutInCertificateFromShed(payload: &str) -> Result<ExchangePutInCertificateFromShed, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let mount_id = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
    
    // Create struct instance
    let result = ExchangePutInCertificateFromShed {
        mount_id,    };
    
    Ok(result)
}

