use anyhow::Context;
use serde::Deserialize;
use std::{collections::{HashMap, HashSet}, fs, path::Path};

#[derive(Deserialize)]
pub struct MappingOverrides {
    pub entries: Vec<OverrideEntry>,
}
#[derive(Deserialize)]
pub struct OverrideEntry {
    pub prefix: String,
    #[allow(dead_code)]
    pub detection_type: Option<String>,
    #[allow(dead_code)]
    pub pattern: Option<String>,
    #[allow(dead_code)]
    pub category: Option<String>,
    pub message_name: Option<String>,
    #[allow(dead_code)]
    pub notes: Option<String>,
}

fn base_alpha(s: &str) -> String {
    s.chars().take_while(|c| c.is_ascii_alphabetic()).collect()
}

/// Prefixes where the symbol is semantically meaningful and MUST NOT be stripped when matching.
fn symbolful_reserved() -> HashSet<&'static str> {
    // Extend this small curated list as needed.
    // Known special: GM|-, BP+, BP-, AM? (from retroproto usage)
    HashSet::from(["GM|-", "BP+", "BP-", "AM?"])
}

/// Parse name/prefix pairs from mappings_go.txt lines like:
///   Name MsgSvrId = "GA"
///   Name = MsgCliId("ping")
pub fn parse_mappings_go(path: &Path) -> HashMap<String, String> {
    let mut map = HashMap::new();
    if !path.exists() { return map; }
    let text = match fs::read_to_string(path) { Ok(t) => t, Err(_) => return map };
    let re_srv = regex::Regex::new(r#"^\s*([A-Za-z0-9_?+-]+)\s+.*=\s*"([^"]+)""#).unwrap();
    let re_cli = regex::Regex::new(r#"^\s*([A-Za-z0-9_?+-]+)\s*=\s*MsgCliId\("([^"]+)"\)"#).unwrap();
    for line in text.lines() {
        if let Some(c) = re_srv.captures(line) {
            let name = c[1].to_string();
            let prefix = c[2].to_string();
            map.insert(prefix, name);
            continue;
        }
        if let Some(c) = re_cli.captures(line) {
            let name = c[1].to_string();
            let prefix = c[2].to_string();
            map.insert(prefix, name);
            continue;
        }
    }
    map
}

/// Build enriched maps:
///  - exact: prefix -> name (from overrides then mappings_go)
///  - exact + base variants (letters-only) unless the exact is in the reserved list (e.g., 'GM|-')
pub fn build_enriched_maps(repo_root: &Path) -> anyhow::Result<(HashMap<String,String>, HashSet<String>)> {
    let mut name_by_prefix: HashMap<String, String> = HashMap::new();

    // 1) load overrides json if present
    let overrides_path = repo_root.join("third_party/retroproto/mapping_overrides.json");
    if overrides_path.exists() {
        let raw = fs::read_to_string(&overrides_path).context("read mapping_overrides.json")?;
        let mo: MappingOverrides = serde_json::from_str(&raw).context("parse mapping_overrides.json")?;
        for e in mo.entries {
            if let Some(n) = e.message_name {
                name_by_prefix.entry(e.prefix).or_insert(n);
            }
        }
    }

    // 2) load mappings_go fallback
    let go_map = parse_mappings_go(&repo_root.join("third_party/retroproto/mappings_go.txt"));
    for (p, n) in go_map {
        name_by_prefix.entry(p).or_insert(n);
    }

    // 3) derive base variants for delimiter-tailed forms (not for reserved symbolful)
    let reserved = symbolful_reserved();
    let mut derived: Vec<(String, String)> = Vec::new();
    for (p, n) in name_by_prefix.iter() {
        let b = base_alpha(p);
        if !b.is_empty() && b != *p && !reserved.contains(p.as_str()) {
            // only add base if base itself isn't already explicitly mapped to a different name
            if !name_by_prefix.contains_key(&b) {
                derived.push((b, n.clone()));
            }
        }
    }
    for (b, n) in derived {
        name_by_prefix.insert(b, n);
    }

    let known: HashSet<String> = name_by_prefix.keys().cloned().collect();
    Ok((name_by_prefix, known))
}