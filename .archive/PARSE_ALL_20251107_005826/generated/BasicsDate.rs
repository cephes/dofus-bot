// AUTO-GENERATED/UPDATED by tools/port_missing_parsers_from_go.py
#![allow(non_snake_case, non_camel_case_types, unused_imports)]
use serde_json::Value;


#[derive(Default, Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct BasicsDate {
    pub Year: i64,
    pub Month: i64,
    pub Day: i64,
}


fn to_i64(s: &str) -> i64 {
    s.trim().parse::<i64>().unwrap_or_default()
}
fn to_f64(s: &str) -> f64 {
    s.trim().parse::<f64>().unwrap_or_default()
}
fn to_bool(s: &str) -> bool {
    match s.trim() {
        "1" | "true" | "True" | "TRUE" => true,
        _ => false,
    }
}
fn split_csv(s: &str) -> Vec<&str> {
    if s.trim().is_empty() { return vec![]; }
    s.split(',').collect()
}


pub fn parse_BasicsDate(payload: &str) -> Result<BasicsDate, String> {
    let parts: Vec<&str> = payload.split(';').collect();
    let mut out = BasicsDate::default();
    let mut idx = 0usize;
    // field: Year : int -> i64
    out.Year = parts.get(idx).map(|s| to_i64(s)).unwrap_or_default();
    idx += 1;
    // field: Month : int -> i64
    out.Month = parts.get(idx).map(|s| to_i64(s)).unwrap_or_default();
    idx += 1;
    // field: Day : int -> i64
    out.Day = parts.get(idx).map(|s| to_i64(s)).unwrap_or_default();
    idx += 1;
    Ok(out)
}


pub fn BasicsDate_to_json(m: &BasicsDate) -> Value { serde_json::to_value(m).unwrap_or(Value::Null) }

