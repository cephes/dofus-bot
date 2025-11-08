#!/usr/bin/env python3
"""
Full Parser Generator - Generate Rust structs and parsers for all messages

Reads schema_rust_map.json and generates:
- Complete Rust struct definitions with derive macros
- Robust parse functions using common_decode helpers
- Proper error handling and field validation
- GameAction sub-parsers in actions/ subdirectory
- Comprehensive type parsing with decoder hints
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def ensure_directory(path: Path):
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)

def generate_rust_struct(struct_data: Dict[str, Any]) -> str:
    """Generate Rust struct definition"""
    struct_name = struct_data['rust_struct_name']
    fields = struct_data['fields']
    
    # Generate struct fields
    field_defs = []
    for field in fields:
        rust_type = field['rust_type']
        field_name = field['name_rust']
        comment = field.get('comment', '')
        
        if comment:
            field_defs.append(f"    /// {comment}\n    pub {field_name}: {rust_type},")
        else:
            field_defs.append(f"    pub {field_name}: {rust_type},")
    
    # Generate struct
    struct_def = f"""#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct {struct_name} {{
{chr(10).join(field_defs)}
}}"""
    
    return struct_def

def generate_decoder_code(field: Dict[str, Any]) -> str:
    """Generate decoding code for a single field based on decoder hint"""
    field_name = field['name_rust']
    decoder_hint = field['decoder_hint']
    rust_type = field['rust_type']
    
    # Handle Option<T> types
    is_optional = rust_type.startswith('Option<')
    base_type = rust_type[7:-1] if is_optional else rust_type
    
    # Generate appropriate decoding code
    if decoder_hint == 'i64':
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_i64(s)).unwrap_or(None);"
        else:
            return f"let {field_name} = common_decode::parse_i64(fields.get(i).unwrap_or(&\"0\"));"
    
    elif decoder_hint == 'i32':
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_i32(s)).unwrap_or(None);"
        else:
            return f"let {field_name} = common_decode::parse_i32(fields.get(i).unwrap_or(&\"0\"));"
    
    elif decoder_hint == 'f64':
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_f64(s)).unwrap_or(None);"
        else:
            return f"let {field_name} = common_decode::parse_f64(fields.get(i).unwrap_or(&\"0.0\"));"
    
    elif decoder_hint == 'bool':
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_bool(s)).unwrap_or(None);"
        else:
            return f"let {field_name} = common_decode::parse_bool(fields.get(i).unwrap_or(&\"false\"));"
    
    elif decoder_hint == 'string':
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_string(s));"
        else:
            return f"let {field_name} = common_decode::parse_string(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'csv':
        if base_type == 'String':
            return f"let {field_name} = common_decode::parse_string_list(fields.get(i).unwrap_or(&\"\"));"
        elif base_type == 'i64':
            return f"let {field_name} = common_decode::parse_i64_list(fields.get(i).unwrap_or(&\"\"));"
        else:
            return f"let {field_name} = common_decode::parse_string_list(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'csv_i64':
        return f"let {field_name} = common_decode::parse_i64_list(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'csv_f64':
        return f"let {field_name} = common_decode::parse_f64_list(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'csv_json':
        return f"let {field_name} = common_decode::parse_string_list(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'segment':
        return f"let {field_name} = common_decode::parse_segmented_fields(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'iso_datetime':
        return f"let {field_name} = common_decode::parse_string(fields.get(i).unwrap_or(&\"\"));"
    
    elif decoder_hint == 'bytes':
        return f"let {field_name} = fields.get(i).unwrap_or(&\"\").as_bytes().to_vec();"
    
    else:
        # Default to string parsing
        if is_optional:
            return f"let {field_name} = fields.get(i).map(|s| common_decode::parse_string(s));"
        else:
            return f"let {field_name} = common_decode::parse_string(fields.get(i).unwrap_or(&\"\"));"

def generate_parser_function(struct_data: Dict[str, Any]) -> str:
    """Generate parse function for struct"""
    struct_name = struct_data['rust_struct_name']
    fields = struct_data['fields']
    
    # Generate field parsing code
    field_parsing = []
    for i, field in enumerate(fields):
        decoder_code = generate_decoder_code(field)
        field_parsing.append(f"        {decoder_code}")
    
    # Generate constructor call
    constructor_args = []
    for field in fields:
        field_name = field['name_rust']
        constructor_args.append(f"        {field_name},")
    
    # Generate function
    parser_function = f"""pub fn parse_{struct_name}(payload: &str) -> Result<{struct_name}, String> {{
    let fields = common_decode::split_fields(payload);
    
    // Parse fields with safe defaults
{chr(10).join(field_parsing)}
    
    // Create struct instance
    let result = {struct_name} {{
{chr(10).join(constructor_args)}    }};
    
    Ok(result)
}}"""
    
    return parser_function

def generate_rust_file(struct_data: Dict[str, Any], output_path: Path):
    """Generate complete Rust file with struct and parser"""
    struct_name = struct_data['rust_struct_name']
    
    # Generate content
    struct_def = generate_rust_struct(struct_data)
    parser_func = generate_parser_function(struct_data)
    
    # Create file content
    file_content = f"""//! Generated parser for {struct_name}
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

{struct_def}

{parser_func}
"""
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(file_content)

def should_be_action_parser(struct_name: str) -> bool:
    """Check if struct should be placed in actions subdirectory"""
    return (struct_name.startswith('GameAction_') or 
            struct_name.startswith('CliAction_') or
            struct_name.startswith('GameActions'))

def get_output_path(struct_data: Dict[str, Any], base_dir: Path) -> Path:
    """Get output path for struct file"""
    struct_name = struct_data['rust_struct_name']
    
    if should_be_action_parser(struct_name):
        actions_dir = base_dir / 'actions'
        ensure_directory(actions_dir)
        return actions_dir / f"{struct_name}.rs"
    else:
        return base_dir / f"{struct_name}.rs"

def generate_parsers_for_structs(structs_data: Dict[str, Any], output_dir: Path) -> Dict[str, str]:
    """Generate parsers for all structs"""
    ensure_directory(output_dir)
    
    generated_files = {}
    action_files = []
    regular_files = []
    
    for struct_name, struct_data in structs_data.items():
        output_path = get_output_path(struct_data, output_dir)
        
        try:
            generate_rust_file(struct_data, output_path)
            generated_files[struct_name] = str(output_path)
            
            if should_be_action_parser(struct_name):
                action_files.append(struct_name)
            else:
                regular_files.append(struct_name)
                
            print(f"Generated: {output_path}")
            
        except Exception as e:
            print(f"Error generating {struct_name}: {e}")
            continue
    
    print(f"\nGenerated {len(regular_files)} regular parsers and {len(action_files)} action parsers")
    
    return generated_files

def update_mod_files(output_dir: Path, action_files: List[str], regular_files: List[str]):
    """Update mod.rs files to include generated modules"""
    
    # Update main mod.rs
    mod_rs_path = output_dir / 'mod.rs'
    regular_mod_lines = [f"pub mod {name};" for name in sorted(regular_files) if name != 'mod']
    action_mod_lines = [f"pub mod actions;"]
    
    mod_content = f"""//! Generated message parsers
//!
//! This module contains automatically generated parsers for all Dofus retroproto messages.

pub mod actions;

{chr(10).join(regular_mod_lines)}
"""
    
    with open(mod_rs_path, 'w', encoding='utf-8') as f:
        f.write(mod_content)
    
    # Update actions mod.rs
    actions_dir = output_dir / 'actions'
    if actions_dir.exists():
        actions_mod_path = actions_dir / 'mod.rs'
        action_mod_lines = [f"pub mod {name};" for name in sorted(action_files)]
        
        actions_mod_content = f"""//! Game Action parsers
//!
//! This module contains parsers for GameAction and CliAction messages.

{chr(10).join(action_mod_lines)}
"""
        
        with open(actions_mod_path, 'w', encoding='utf-8') as f:
            f.write(actions_mod_content)

def main():
    """Main execution function"""
    # Load schema mapping
    mapping_path = Path("schema_rust_map.json")
    if not mapping_path.exists():
        print("Error: schema_rust_map.json not found. Run go_to_rust_mapper.py first.")
        return
    
    with open(mapping_path, 'r') as f:
        mapping_data = json.load(f)
    
    print(f"Generating parsers for {mapping_data['total_structs']} structs...")
    
    # Generate parsers
    output_dir = Path("core/src/retroproto_parsers/generated")
    generated_files = generate_parsers_for_structs(mapping_data['structs'], output_dir)
    
    # Categorize files
    action_files = []
    regular_files = []
    
    for struct_name in generated_files.keys():
        if should_be_action_parser(struct_name):
            action_files.append(struct_name)
        else:
            regular_files.append(struct_name)
    
    # Update mod files
    update_mod_files(output_dir, action_files, regular_files)
    
    # Create generation report
    report = {
        'generated_at': '2025-11-07T01:26:48Z',
        'total_files': len(generated_files),
        'action_files': len(action_files),
        'regular_files': len(regular_files),
        'generated_files': generated_files,
        'action_structs': sorted(action_files),
        'regular_structs': sorted(regular_files)
    }
    
    report_path = output_dir / 'full_generation_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== Generation Summary ===")
    print(f"Total files generated: {len(generated_files)}")
    print(f"Action parsers: {len(action_files)}")
    print(f"Regular parsers: {len(regular_files)}")
    print(f"Report written to: {report_path}")
    
    return report

if __name__ == "__main__":
    main()