//! Generated parser for ExchangeMountStorageRemove
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct ExchangeMountStorageRemove {
    /// Dofus ID
    pub mount_id: i64,
}

pub fn parse_ExchangeMountStorageRemove(payload: &str) -> Result<ExchangeMountStorageRemove, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let mount_id = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
    
    // Create struct instance
    let result = ExchangeMountStorageRemove {
        mount_id,    };
    
    Ok(result)
}
