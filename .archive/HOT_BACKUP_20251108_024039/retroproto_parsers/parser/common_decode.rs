//! Common decoding utilities for Dofus retroproto message parsing
//! 
//! This module provides robust decoders for common Dofus encoding patterns:
//! - `;` field separators
//! - `,` list separators  
//! - `~` segment separators
//! - `^` pair separators
//! - `|-` removal forms
//! - empty string → default values

#![allow(non_snake_case)]
use std::collections::HashMap;

/// Split a payload by semicolon separators, handling empty fields
pub fn split_fields(payload: &str) -> Vec<&str> {
    if payload.is_empty() {
        return Vec::new();
    }
    payload.split(';').into_iter().collect()
}

/// Split a string by comma separators, handling empty fields
pub fn split_csv(s: &str) -> Vec<&str> {
    if s.is_empty() {
        return Vec::new();
    }
    s.split(',').into_iter().collect()
}

/// Split a string by a custom separator, handling empty fields
pub fn split_segments(s: &str, sep: char) -> Vec<&str> {
    if s.is_empty() {
        return Vec::new();
    }
    s.split(sep).into_iter().collect()
}

/// Parse an i64 from a string, with safe defaults
pub fn parse_i64(s: &str) -> i64 {
    let trimmed = s.trim();
    if trimmed.is_empty() {
        return 0;
    }
    trimmed.parse::<i64>().unwrap_or(0)
}

/// Parse a bool from a string with flexible interpretation
pub fn parse_bool(s: &str) -> bool {
    let trimmed = s.trim().to_lowercase();
    match trimmed.as_str() {
        "1" | "true" | "yes" | "on" | "enabled" => true,
        "0" | "false" | "no" | "off" | "disabled" => false,
        _ => false,
    }
}

/// Parse a string, trimming whitespace
pub fn parse_string(s: &str) -> String {
    s.trim().to_string()
}

/// Parse a list of i64 values from a comma-separated string
pub fn parse_i64_list(s: &str) -> Vec<i64> {
    split_csv(s).iter().map(|&x| parse_i64(x)).into_iter().collect()
}

/// Parse a list of strings from a comma-separated string
pub fn parse_string_list(s: &str) -> Vec<String> {
    split_csv(s).iter().map(|&x| parse_string(x)).into_iter().collect()
}

/// Parse a key-value pair separated by ^
pub fn parse_kv_pair(s: &str) -> (String, String) {
    let parts: Vec<&str> = split_segments(s, '^').into_iter().collect();
    match parts.as_slice() {
        [key, value] => (parse_string(key), parse_string(value)),
        _ => (s.trim().to_string(), String::new()),
    }
}

/// Parse a list of key-value pairs
pub fn parse_kv_pairs(s: &str) -> HashMap<String, String> {
    let mut result = HashMap::new();
    for pair in split_csv(s) {
        let (key, value) = parse_kv_pair(pair);
        if !key.is_empty() {
            result.insert(key, value);
        }
    }
    result
}

/// Parse optional removal indicators (|- prefix)
pub fn parse_removal_flag(s: &str) -> (bool, String) {
    if s.starts_with("|-") {
        (true, s[2..].to_string())
    } else {
        (false, s.to_string())
    }
}

/// Safe i32 parsing
pub fn parse_i32(s: &str) -> i32 {
    let trimmed = s.trim();
    if trimmed.is_empty() {
        return 0;
    }
    trimmed.parse::<i32>().unwrap_or(0)
}

/// Safe f64 parsing
pub fn parse_f64(s: &str) -> f64 {
    let trimmed = s.trim();
    if trimmed.is_empty() {
        return 0.0;
    }
    trimmed.parse::<f64>().unwrap_or(0.0)
}

/// Parse comma-separated list of f64 values
pub fn parse_f64_list(s: &str) -> Vec<f64> {
    split_csv(s).iter().map(|&x| parse_f64(x)).into_iter().collect()
}

/// Handle segmented payloads that may contain ~ sub-blocks
pub fn parse_segmented_fields(s: &str) -> Vec<String> {
    split_segments(s, '~').iter().map(|&x| parse_string(x)).into_iter().collect()
}

/// Parse payload that may contain both semicolon and segment delimiters
pub fn parse_complex_payload(payload: &str) -> Vec<Vec<String>> {
    let main_fields = split_fields(payload);
    main_fields.iter().map(|&field| {
        if field.contains('~') {
            parse_segmented_fields(field)
        } else {
            vec![parse_string(field)]
        }
    }).into_iter().collect()
}

/// Safe default for optional numeric fields
pub fn default_i64() -> i64 { 0 }
pub fn default_i32() -> i32 { 0 }
pub fn default_f64() -> f64 { 0.0 }
pub fn default_string() -> String { String::new() }
pub fn default_bool() -> bool { false }
pub fn default_vec_i64() -> Vec<i64> { Vec::new() }
pub fn default_vec_string() -> Vec<String> { Vec::new() }
pub fn default_kv_map() -> HashMap<String, String> { HashMap::new() }

/// Parse with error recovery - returns parsed value or default
pub fn parse_or_default<T: Default>(s: &str, parser: fn(&str) -> T) -> T {
    let trimmed = s.trim();
    if trimmed.is_empty() {
        return T::default();
    }
    parser(trimmed)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_split_fields() {
        assert_eq!(split_fields("field1;field2;field3"), vec!["field1", "field2", "field3"]);
        assert_eq!(split_fields(""), Vec::<&str>::new());
        assert_eq!(split_fields("single"), vec!["single"]);
    }

    #[test]
    fn test_split_csv() {
        assert_eq!(split_csv("a,b,c"), vec!["a", "b", "c"]);
        assert_eq!(split_csv(""), Vec::<&str>::new());
    }

    #[test]
    fn test_parse_i64() {
        assert_eq!(parse_i64("123"), 123);
        assert_eq!(parse_i64(""), 0);
        assert_eq!(parse_i64("invalid"), 0);
        assert_eq!(parse_i64("  456  "), 456);
    }

    #[test]
    fn test_parse_bool() {
        assert_eq!(parse_bool("1"), true);
        assert_eq!(parse_bool("true"), true);
        assert_eq!(parse_bool("0"), false);
        assert_eq!(parse_bool("false"), false);
        assert_eq!(parse_bool("invalid"), false);
    }

    #[test]
    fn test_parse_kv_pair() {
        assert_eq!(parse_kv_pair("key^value"), ("key".to_string(), "value".to_string()));
        assert_eq!(parse_kv_pair("single"), ("single".to_string(), String::new()));
    }

    #[test]
    fn test_parse_removal_flag() {
        assert_eq!(parse_removal_flag("|-removed"), (true, "removed".to_string()));
        assert_eq!(parse_removal_flag("normal"), (false, "normal".to_string()));
    }

    #[test]
    fn test_parse_i64_list() {
        assert_eq!(parse_i64_list("1,2,3"), vec![1, 2, 3]);
        assert_eq!(parse_i64_list(""), Vec::<i64>::new());
    }

    #[test]
    fn test_parse_kv_pairs() {
        let result = parse_kv_pairs("a^1,b^2");
        let mut expected = HashMap::new();
        expected.insert("a".to_string(), "1".to_string());
        expected.insert("b".to_string(), "2".to_string());
        assert_eq!(result, expected);
    }
}