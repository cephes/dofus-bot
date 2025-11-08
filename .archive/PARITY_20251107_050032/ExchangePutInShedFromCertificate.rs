//! Generated parser for ExchangePutInShedFromCertificate
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangePutInShedFromCertificate {
    /// Dofus ID
    pub certificate_id: i64,
}

pub fn parse_ExchangePutInShedFromCertificate(payload: &str) -> Result<ExchangePutInShedFromCertificate, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let certificate_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangePutInShedFromCertificate {
        certificate_id,    };
    
    Ok(result)
}
