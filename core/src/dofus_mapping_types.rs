use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct MappingOverrides {
    pub entries: Vec<MappingEntry>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct MappingEntry {
    pub prefix: String,
    #[allow(dead_code)]
    pub detection_type: Option<String>,
    #[allow(dead_code)]
    pub pattern: Option<String>,
    pub category: Option<String>,
    pub example_payload: Option<String>,
    pub notes: Option<String>,
    pub message_name: Option<String>,
}