//! Generated parser for DocumentsCreateError
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct DocumentsCreateError {

}

pub fn parse_DocumentsCreateError(payload: &str) -> Result<DocumentsCreateError, String> {
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults

    
    // Create struct instance
    let result = DocumentsCreateError {
    };
    
    Ok(result)
}
