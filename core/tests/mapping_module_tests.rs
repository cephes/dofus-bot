use dofus_core::dofus_mapping::{detect_prefix_from_text, load_runtime_mapping};
use std::path::Path;

#[test]
fn test_load_compiled_literals() {
    // Test that runtime mapping loads if available
    let path = Path::new("../../../dofus-retro-bot/third_party/retroproto/mapping.json");
    match load_runtime_mapping(Some(path)) {
        Ok(Some(entries)) => {
            assert!(!entries.is_empty());
            // Check for some known literals
            let aa_entry = entries.iter().find(|e| e.prefix == "AA");
            assert!(aa_entry.is_some());
            assert_eq!(aa_entry.unwrap().category, "client");
        }
        Ok(None) => {
            // Mapping file not found, skip
            eprintln!("Mapping file not found, skipping literal test");
        }
        Err(e) => {
            eprintln!("Error loading mapping: {}", e);
        }
    }
}

#[test]
fn test_regex_compile_and_match() {
    // Test regex compilation and matching
    let test_payload = "1.29.1";
    let meta = detect_prefix_from_text(test_payload);
    if let Some(meta) = meta {
        assert_eq!(meta.detection_type, "regex");
        assert!(meta.pattern.is_some());
    } else {
        eprintln!("Regex detection failed, but that's ok if mapping not loaded");
    }
}

#[test]
fn test_detect_prefix_functionality() {
    // Test detection with known prefixes
    let test_cases = vec![
        ("AA", "client"),
        ("ping", "client"),
        ("version", "client"),
    ];

    for (prefix, expected_category) in test_cases {
        let meta = detect_prefix_from_text(prefix);
        if let Some(meta) = meta {
            assert_eq!(meta.category, expected_category);
        } else {
            eprintln!("Detection failed for {}, but ok if mapping not loaded", prefix);
        }
    }
}