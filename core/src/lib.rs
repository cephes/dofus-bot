#![allow(
    non_snake_case,
    non_camel_case_types,
    non_upper_case_globals,
    clippy::all,
    clippy::pedantic,
    clippy::nursery,
    unused_imports,
    dead_code
)]

pub mod dofus_framing;
pub mod dofus_mapping;
pub mod dofus_mapping_ext;
pub mod dofus_mapping_types;
pub mod dofus_proto;
pub mod parser;
pub mod retroproto_parsers;
pub mod ids;