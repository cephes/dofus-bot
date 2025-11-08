//! Generated parser for AccountStats
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountStats {
    /// Experience points
    pub xp: i64,
    /// Experience points
    pub xp_low: i64,
    /// Experience points
    pub xp_high: i64,
    pub kama: i64,
    pub bonus_points: i64,
    pub bonus_points_spell: i64,
    pub alignment: i64,
    pub fake_alignment: i64,
    /// Level
    pub alignment_level: i32,
    pub grade: i64,
    pub honour: i64,
    pub disgrace: i64,
    /// Boolean flag
    pub alignment_enabled: bool,
    pub lp: i64,
    pub lp_max: i64,
    pub energy: i64,
    pub energy_max: i64,
    pub initiative: i64,
    pub discernment: i64,
    /// Unknown type map
    pub characteristics: String,
}

pub fn parse_AccountStats(payload: &str) -> Result<AccountStats, String> {
    let mut i = 0;
    let _fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
        let xp = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let xp_low = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let xp_high = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let kama = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let bonus_points = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let bonus_points_spell = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let alignment = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let fake_alignment = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let alignment_level = common_decode::parse_i32(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let grade = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let honour = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let disgrace = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let alignment_enabled = common_decode::parse_bool(_fields.get(i).unwrap_or(&"false"));
        i += 1;
        let lp = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let lp_max = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let energy = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let energy_max = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let initiative = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let discernment = common_decode::parse_i64(_fields.get(i).unwrap_or(&"0"));
        i += 1;
        let characteristics = common_decode::parse_string(_fields.get(i).unwrap_or(&""));
        i += 1;
    
    // Create struct instance
    let result = AccountStats {
        xp,
        xp_low,
        xp_high,
        kama,
        bonus_points,
        bonus_points_spell,
        alignment,
        fake_alignment,
        alignment_level,
        grade,
        honour,
        disgrace,
        alignment_enabled,
        lp,
        lp_max,
        energy,
        energy_max,
        initiative,
        discernment,
        characteristics,    };
    
    Ok(result)
}
