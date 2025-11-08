use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use once_cell::sync::Lazy;
use regex::Regex;
use std::path::Path;
use anyhow::Result;
use std::fs;
use crate::dofus_mapping_types::MappingOverrides;
static MAP_PATH: &str = "third_party/retroproto/mapping_overrides.json";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MessageMeta {
    pub prefix: String,
    pub category: String,
    pub detection_type: String,
    pub pattern: Option<String>,
    pub source_file: Option<String>,
    pub source_line: Option<u64>,
    pub example_payload: Option<String>,
    pub notes: Option<String>,
    pub manual_review: Option<bool>,
}

static LITERAL_MAPPING: Lazy<HashMap<&'static str, MessageMeta>> = Lazy::new(|| {
    let map = HashMap::new();
    // Compile-time fallback literals (empty for now, populated from JSON if available)
    map
});

static REGEX_MAPPING: Lazy<Vec<(Regex, MessageMeta)>> = Lazy::new(|| {
    vec![
        // Compile-time fallback regexes (empty for now)
    ]
});

pub fn load_runtime_mapping(path: Option<&Path>) -> Result<Option<Vec<MessageMeta>>> {
    let default_path = Path::new("../../../dofus-retro-bot/third_party/retroproto/mapping.json");
    let path = path.unwrap_or(default_path);

    if path.exists() {
        let content = std::fs::read_to_string(path)?;
        let mapping: serde_json::Value = serde_json::from_str(&content)?;
        let entries: Vec<MessageMeta> = serde_json::from_value(mapping["entries"].clone())?;
        Ok(Some(entries))
    } else {
        Ok(None)
    }
}

pub fn detect_prefix_from_text(s: &str) -> Option<MessageMeta> {
    if s.is_empty() {
        return None;
    }

    // Normalize: take first few chars for prefix detection
    let prefix_candidate = &s[..std::cmp::min(s.len(), 10)];

    // Check literals first (fast)
    if let Some(meta) = LITERAL_MAPPING.get(prefix_candidate) {
        return Some(meta.clone());
    }

    // Check runtime literals if loaded
    if let Ok(Some(runtime_entries)) = load_runtime_mapping(None) {
        for entry in runtime_entries {
            if entry.detection_type == "literal" && s.starts_with(&entry.prefix) {
                return Some(entry);
            }
        }
    }

    // Check regexes
    for (regex, meta) in &*REGEX_MAPPING {
        if regex.is_match(s) {
            return Some(meta.clone());
        }
    }

    // Check runtime regexes
    if let Ok(Some(runtime_entries)) = load_runtime_mapping(None) {
        for entry in runtime_entries {
            if entry.detection_type == "regex" {
                if let Some(pattern) = &entry.pattern {
                    if let Ok(regex) = Regex::new(pattern) {
                        if regex.is_match(s) {
                            return Some(entry);
                        }
                    }
                }
            }
        }
    }

    None
}

/// Load mapping_overrides.json (authoritative prefixes).
pub fn load_mapping_overrides() -> anyhow::Result<MappingOverrides> {
    let p = Path::new(MAP_PATH);
    let s = fs::read_to_string(p)?;
    let data: MappingOverrides = serde_json::from_str(&s)?;
    Ok(data)
}

/// Return all known prefixes (client + server) as Vec<String>.
pub fn all_known_prefixes() -> Vec<String> {
    if let Ok(m) = load_mapping_overrides() {
        let mut v: Vec<String> = m.entries.iter().map(|e| e.prefix.clone()).collect();
        v.sort();
        v.dedup();
        v
    } else {
        Vec::new()
    }
}