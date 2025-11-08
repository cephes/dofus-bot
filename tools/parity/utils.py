"""
Utilities for the parity loop system.
"""
import json
import os
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union


def ts() -> str:
    """Generate timestamp string in YYYYMMDD_HHMMSS format."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dirs(paths: List[str]) -> None:
    """Ensure all directories exist."""
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    """Read JSONL file and return list of dictionaries."""
    result = []
    if not os.path.exists(path):
        return result
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    result.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return result


def read_json(path: str) -> Any:
    """Read JSON file and return parsed content."""
    if not os.path.exists(path):
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, obj: Any) -> None:
    """Write JSON file with proper formatting."""
    ensure_dirs([os.path.dirname(path)])
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def write_text(path: str, content: str) -> None:
    """Write text file."""
    ensure_dirs([os.path.dirname(path)])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def copy_tree(src: str, dst: str) -> None:
    """Copy directory tree recursively."""
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


def list_parser_file(message_name: str, core_path: str = "core") -> str:
    """Get absolute path to the Rust parser file for a message name."""
    base_path = f"{core_path}/src/retroproto_parsers/generated"
    
    # Check for action parsers
    if message_name.startswith('GameAction') or message_name.startswith('CliAction'):
        return f"{base_path}/actions/{message_name}.rs"
    else:
        return f"{base_path}/{message_name}.rs"


def snake_case(s: str) -> str:
    """Convert camelCase/PascalCase to snake_case."""
    # Insert underscores between lowercase and uppercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    # Insert underscores between consecutive uppercase letters
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def rust_type_for_json(value: Any) -> str:
    """Infer Rust type from JSON value."""
    if value is None:
        return "String"  # Will be wrapped in Option<T> by caller
    
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "i64"
    elif isinstance(value, float):
        return "f64"
    elif isinstance(value, str):
        return "String"
    elif isinstance(value, list):
        if not value:
            return "Vec<String>"
        
        # Determine homogeneous type from first element
        if value:
            first_type = rust_type_for_json(value[0])
            return f"Vec<{first_type}>"
        return "Vec<String>"
    elif isinstance(value, dict):
        # For objects, we'll use a conservative approach
        return "String"  # Store as JSON string if we can't map fields
    else:
        return "String"


def patch_struct_fields(file_text: str, field_order_types: List[Tuple[str, str]]) -> str:
    """Patch struct fields with missing fields and proper ordering."""
    lines = file_text.split('\n')
    
    # Find the struct definition
    struct_start = -1
    struct_end = -1
    brace_count = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('pub struct ') and '{' in stripped:
            struct_start = i
            brace_count = stripped.count('{') - stripped.count('}')
            continue
        elif struct_start >= 0:
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0 and '}' in line:
                struct_end = i
                break
    
    if struct_start < 0 or struct_end < 0:
        return file_text  # No struct found
    
    # Extract current fields
    current_fields = {}
    for i in range(struct_start + 1, struct_end):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('pub ') and ':' in stripped:
            parts = stripped.split(':', 1)
            if len(parts) == 2:
                field_name = parts[0].replace('pub ', '').strip()
                field_type = parts[1].rstrip(',').strip()
                current_fields[field_name] = field_type
    
    # Create new field list
    new_fields = []
    for field_name, field_type in field_order_types:
        if field_name in current_fields:
            new_fields.append(f"    pub {field_name}: {current_fields[field_name]},")
        else:
            new_fields.append(f"    pub {field_name}: {field_type},")
    
    # Add any remaining current fields that weren't in the order list
    for field_name, field_type in current_fields.items():
        if not any(name == field_name for name, _ in field_order_types):
            new_fields.append(f"    pub {field_name}: {field_type},")
    
    # Rebuild the struct
    new_lines = lines[:struct_start + 1] + new_fields + [''] + lines[struct_end:]
    return '\n'.join(new_lines)


def patch_parse_body_csv(file_text: str, field_names_in_order: List[str]) -> str:
    """Patch parse function body for CSV-style parsing."""
    lines = file_text.split('\n')
    
    # Find the parse function
    func_start = -1
    func_end = -1
    brace_count = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('pub fn parse('):
            func_start = i
            brace_count = stripped.count('{') - stripped.count('}')
            continue
        elif func_start >= 0:
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0 and '}' in line:
                func_end = i
                break
    
    if func_start < 0 or func_end < 0:
        return file_text  # No function found
    
    # Generate new parse body
    new_body = [
        "        let parts: Vec<&str> = payload.split(';').collect();",
        ""
    ]
    
    for i, field_name in enumerate(field_names_in_order):
        snake_name = snake_case(field_name)
        new_body.append(f"        let {snake_name} = parts.get({i}).map(|s| s.trim()).unwrap_or_default().parse::<i64>().unwrap_or(0);")
    
    new_body.append("")
    new_body.append("        Ok(Self {")
    for field_name in field_names_in_order:
        snake_name = snake_case(field_name)
        new_body.append(f"            {snake_name},")
    new_body.append("        })")
    
    # Replace the function body
    new_lines = lines[:func_start + 1] + new_body + [''] + lines[func_end:]
    return '\n'.join(new_lines)


def patch_parse_body_json_passthrough(file_text: str, json_field_map: Dict[str, str]) -> str:
    """Patch parse function for JSON passthrough."""
    lines = file_text.split('\n')
    
    # Find the parse function
    func_start = -1
    func_end = -1
    brace_count = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('pub fn parse('):
            func_start = i
            brace_count = stripped.count('{') - stripped.count('}')
            continue
        elif func_start >= 0:
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0 and '}' in line:
                func_end = i
                break
    
    if func_start < 0 or func_end < 0:
        return file_text  # No function found
    
    # Generate new parse body for passthrough
    new_body = [
        "        // Conservative passthrough parsing",
        "        let raw = payload.to_string();",
        ""
    ]
    
    if json_field_map:
        new_body.append("        let mut result = Self {")
        for field_name in field_names_in_order if 'field_names_in_order' in locals() else json_field_map.keys():
            snake_name = snake_case(field_name)
            new_body.append(f"            {snake_name}: None,")
        new_body.append("            raw,")
        new_body.append("        };")
        new_body.append("")
        new_body.append("        // TODO: Implement field extraction logic")
        new_body.append("        Ok(result)")
    else:
        new_body.append("        Ok(Self {")
        new_body.append("            raw,")
        new_body.append("        })")
    
    # Replace the function body
    new_lines = lines[:func_start + 1] + new_body + [''] + lines[func_end:]
    return '\n'.join(new_lines)


def rewrite_mod_rs_if_needed(mod_rs_path: str) -> bool:
    """Update mod.rs to ensure correct module declarations."""
    if not os.path.exists(mod_rs_path):
        return False
    
    with open(mod_rs_path, 'r') as f:
        content = f.read()
    
    # Check if actions module is declared
    if 'pub mod actions;' not in content:
        lines = content.split('\n')
        new_lines = []
        actions_added = False
        
        for line in lines:
            if line.strip().startswith('// Action') and not actions_added:
                new_lines.append('pub mod actions;')
                new_lines.append('')
                actions_added = True
            
            new_lines.append(line)
        
        if not actions_added:
            new_lines.insert(0, 'pub mod actions;')
            new_lines.insert(1, '')
        
        with open(mod_rs_path, 'w') as f:
            f.write('\n'.join(new_lines))
        return True
    
    return False