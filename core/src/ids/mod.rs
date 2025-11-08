#![allow(clippy::missing_const_for_fn)]
use once_cell::sync::Lazy;
use serde::Deserialize;
use std::collections::HashMap;

#[derive(Deserialize)]
struct StrMap(HashMap<String, String>);

fn load_map(included: &str) -> HashMap<i32, &'static str> {
    let raw: HashMap<String, String> = serde_json::from_str(included)
        .expect("ids JSON malformed");
    // Leak strings to get &'static str (tiny memory cost, fast lookups)
    raw.into_iter().map(|(k, v)| {
        let kid = k.parse::<i32>().unwrap_or_else(|_| panic!("bad id key {}", k));
        let vs: &'static str = Box::leak(v.into_boxed_str());
        (kid, vs)
    }).collect()
}

pub static MONSTERS: Lazy<HashMap<i32, &'static str>> = Lazy::new(|| {
    load_map(include_str!("../../assets/ids/monsters.json"))
});
pub static SPELLS: Lazy<HashMap<i32, &'static str>> = Lazy::new(|| {
    load_map(include_str!("../../assets/ids/spells.json"))
});
pub static ITEMS: Lazy<HashMap<i32, &'static str>> = Lazy::new(|| {
    load_map(include_str!("../../assets/ids/items.json"))
});
pub static JOBS: Lazy<HashMap<i32, &'static str>> = Lazy::new(|| {
    load_map(include_str!("../../assets/ids/jobs.json"))
});
pub static INTERACTIVES: Lazy<HashMap<i32, &'static str>> = Lazy::new(|| {
    load_map(include_str!("../../assets/ids/interactives.json"))
});

#[inline] pub fn monster_name(id: i32) -> Option<&'static str> { MONSTERS.get(&id).copied() }
#[inline] pub fn spell_name(id: i32) -> Option<&'static str> { SPELLS.get(&id).copied() }
#[inline] pub fn item_name(id: i32) -> Option<&'static str> { ITEMS.get(&id).copied() }
#[inline] pub fn job_name(id: i32) -> Option<&'static str> { JOBS.get(&id).copied() }
#[inline] pub fn interactive_name(id: i32) -> Option<&'static str> { INTERACTIVES.get(&id).copied() }

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn smoke_maps_loaded() {
        // Maps can be empty if source files were missing; just assert no panic.
        let _ = MONSTERS.len() + SPELLS.len() + ITEMS.len() + JOBS.len() + INTERACTIVES.len();
    }
}