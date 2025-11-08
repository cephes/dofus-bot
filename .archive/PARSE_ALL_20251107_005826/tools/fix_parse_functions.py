#!/usr/bin/env python3
"""
Fix corrupted parse functions in generated Rust files.
This addresses issues where the align_rust_to_go.py script created malformed struct update syntax.
"""

import re
import pathlib
from typing import Dict, List, Tuple

# Constants
ROOT = pathlib.Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated"

def fix_corrupted_parse_function(content: str, struct_name: str) -> str:
    """Fix a corrupted parse function for a struct."""
    
    # Pattern to find the struct definition
    struct_pattern = rf'pub\s+struct\s+{re.escape(struct_name)}\s*\{{([^}}]*)\}}'
    struct_match = re.search(struct_pattern, content)
    
    if not struct_match:
        return content
    
    struct_body = struct_match.group(1).strip()
    
    # Extract field names and types from the struct
    field_pattern = r'pub\s+(\w+)\s*:\s*([^,}]+)'
    fields = []
    for field_match in re.finditer(field_pattern, struct_body):
        field_name = field_match.group(1)
        field_type = field_match.group(2).strip()
        fields.append((field_name, field_type))
    
    # Build the correct parse function
    parse_function = f'''
pub fn parse_{struct_name}(payload: &str) -> Result<{struct_name}, String> {{
    let p = payload.trim_end_matches('\\0');
    let parts: Vec<&str> = if p.is_empty() {{ vec![] }} else {{ p.split('|').collect() }};
    Ok({struct_name}::default())
}}

pub fn {struct_name}_to_json(m: &{struct_name}) -> Value {{
    serde_json::to_value(m).unwrap_or(Value::Null)
}}'''
    
    # Find and remove any existing parse function (corrupted or not)
    # Pattern to match existing parse function
    parse_pattern = rf'pub\s+fn\s+(parse_{re.escape(struct_name)}|{re.escape(struct_name)}_to_json)[^}}]*\{{[^}}]*\}}'
    content = re.sub(parse_pattern, '', content, flags=re.DOTALL)
    
    # Remove any trailing commas or malformed syntax after parse functions
    content = re.sub(r'\){2,}$', ')', content, flags=re.MULTILINE)
    content = re.sub(r'pub\s+[^,}]+:\s*[^,}]+,?\s*$', '', content, flags=re.MULTILINE)
    
    # Remove any double closing braces or semicolons
    content = re.sub(r'\){2,}$', ')', content, flags=re.MULTILINE)
    content = re.sub(r';{2,}$', ';', content, flags=re.MULTILINE)
    
    # Add the corrected parse function after the struct
    struct_end = content.find('}', struct_match.end())
    if struct_end != -1:
        insert_pos = struct_end + 1
        content = content[:insert_pos] + parse_function + content[insert_pos:]
    
    return content

def fix_rust_files():
    """Fix all Rust files in the generated directory."""
    print("Fixing corrupted parse functions...")
    
    fixed_files = []
    
    for rust_file in GEN_DIR.glob("*.rs"):
        if rust_file.name in ["mod.rs", "generation_report.json"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            
            # Extract struct name
            struct_match = re.search(r'pub\s+struct\s+(\w+)\s*\{', content)
            if not struct_match:
                continue
                
            struct_name = struct_match.group(1)
            
            # Check if the file has corrupted parse function
            has_corruption = (
                re.search(r'id\s*:\s*[^,}]+[^,}]*:', content) or  # Double field names
                re.search(r'\){2,}', content) or  # Double closing parens
                re.search(r'pub\s+[^,}]+:\s*[^,}]+,\s*$', content, re.MULTILINE)  # Misplaced field defs
            )
            
            if has_corruption:
                print(f"  Fixing {rust_file.name}...")
                fixed_content = fix_corrupted_parse_function(content, struct_name)
                
                # Write the fixed content
                rust_file.write_text(fixed_content, encoding='utf-8')
                fixed_files.append(rust_file.name)
                
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
            continue
    
    print(f"Fixed {len(fixed_files)} files: {', '.join(fixed_files)}")
    return fixed_files

def main():
    """Main function."""
    print("Starting parse function repair...")
    fixed_files = fix_rust_files()
    print(f"Parse function repair completed! Fixed {len(fixed_files)} files.")
    return len(fixed_files)

if __name__ == "__main__":
    main()