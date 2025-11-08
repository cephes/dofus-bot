//! Generated parser for DialogQuestion
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
use serde::{Serialize, Deserialize};
pub struct DialogQuestion {
    pub question: i64,
    /// CSV list
    pub question_params: Vec<String>,
    /// CSV list of integers
    pub answers: Vec<i64>,
}

pub fn parse_DialogQuestion(payload: &str) -> Result<DialogQuestion, String> {
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let question = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));
        let question_params = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));
        let answers = common_decode::parse_i64_list(fields.get(i).unwrap_or(&""));
    
    // Create struct instance
    let result = DialogQuestion {
        question,
        question_params,
        answers,    };
    
    Ok(result)
}

