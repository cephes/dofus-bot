#!/usr/bin/env python3
"""
Go to Rust Mapper - Map Go types to Rust types with decoder hints

Reads schema_index.json and produces a mapping JSON with:
- Rust type mappings
- Decoder hints for parsing logic
- Field name conversions
- Type annotations for code generation
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Try to import yaml, make it optional
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Load existing overrides if available
def load_overrides(overrides_file: str = "tools/decoder_overrides.yaml") -> Dict[str, Any]:
    """Load decoder overrides from YAML file"""
    overrides_path = Path(overrides_file)
    if overrides_path.exists():
        try:
            if YAML_AVAILABLE:
                with open(overrides_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                # Simple JSON fallback if YAML not available
                with open(overrides_path, 'r') as f:
                    content = f.read().strip()
                    if content and content != '{}':
                        print("Warning: YAML module not available, skipping overrides file")
                    return {}
        except Exception as e:
            print(f"Warning: Could not load overrides: {e}")
    return {}

def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_rust_type(go_type: str, is_pointer: bool, is_slice: bool, field_name: str, overrides: Dict[str, Any]) -> tuple[str, str, str]:
    """Map Go type to Rust type with decoder hint"""
    
    # Check for field-specific overrides
    field_override_key = f"{field_name}.rust_type"
    if field_override_key in overrides:
        override = overrides[field_override_key]
        return override.get('rust_type', 'String'), override.get('decoder_hint', 'as-is'), override.get('comment', '')
    
    # Base type mappings
    base_mappings = {
        'string': ('String', 'string', ''),
        'int': ('i64', 'i64', ''),
        'int32': ('i32', 'i32', ''),
        'int64': ('i64', 'i64', ''),
        'uint': ('u64', 'u64', ''),
        'uint32': ('u32', 'u32', ''),
        'uint64': ('u64', 'u64', ''),
        'bool': ('bool', 'bool', ''),
        'float': ('f64', 'f64', ''),
        'float64': ('f64', 'f64', ''),
        'time.Time': ('String', 'iso_datetime', ''),
        '[]byte': ('Vec<u8>', 'bytes', ''),
    }
    
    # Handle []Type slices
    if is_slice:
        if go_type == 'string':
            return ('Vec<String>', 'csv', 'CSV list')
        elif go_type in ['int', 'int64', 'int32']:
            return ('Vec<i64>', 'csv_i64', 'CSV list of integers')
        elif go_type in ['uint', 'uint64', 'uint32']:
            return ('Vec<u64>', 'csv_u64', 'CSV list of unsigned integers')
        elif go_type in ['float', 'float64']:
            return ('Vec<f64>', 'csv_f64', 'CSV list of floats')
        else:
            return (f'Vec<{go_type}>', 'csv_json', 'CSV list (JSON encoded)')
    
    # Handle *Type pointers (optional)
    if is_pointer:
        if go_type == 'string':
            return ('Option<String>', 'optional_string', 'Optional string')
        elif go_type in ['int', 'int64', 'int32']:
            return ('Option<i64>', 'optional_i64', 'Optional integer')
        elif go_type in ['bool']:
            return ('Option<bool>', 'optional_bool', 'Optional boolean')
        else:
            return (f'Option<{go_type}>', 'optional', f'Optional {go_type}')
    
    # Check for known Dofus types with special parsing
    if 'id' in field_name.lower():
        return ('i64', 'i64', 'Dofus ID')
    elif 'ids' in field_name.lower():
        return ('Vec<i64>', 'csv', 'CSV list of IDs')
    elif 'position' in field_name.lower() and 's' in field_name.lower():
        return ('Vec<i64>', 'csv', 'Position list')
    elif 'cell' in field_name.lower():
        return ('i32', 'i32', 'Map cell number')
    elif 'color' in field_name.lower():
        return ('i32', 'i32', 'Color value')
    elif 'timer' in field_name.lower() or 'time' in field_name.lower():
        return ('i64', 'i64', 'Timestamp/milliseconds')
    elif 'duration' in field_name.lower():
        return ('i64', 'i64', 'Duration in milliseconds')
    elif 'name' in field_name.lower():
        return ('String', 'string', 'Name/label')
    elif 'message' in field_name.lower() or 'text' in field_name.lower():
        return ('String', 'string', 'Text message')
    elif 'amount' in field_name.lower() or 'value' in field_name.lower():
        return ('i64', 'i64', 'Numeric value')
    elif 'kamas' in field_name.lower():
        return ('i64', 'i64', 'Kamas (currency)')
    elif 'level' in field_name.lower():
        return ('i32', 'i32', 'Level')
    elif 'experience' in field_name.lower() or 'xp' in field_name.lower():
        return ('i64', 'i64', 'Experience points')
    elif 'percent' in field_name.lower() or 'percentage' in field_name.lower():
        return ('f64', 'f64', 'Percentage (0.0-1.0)')
    elif 'count' in field_name.lower() or 'number' in field_name.lower():
        return ('i32', 'i32', 'Count/number')
    elif 'flag' in field_name.lower() or 'enabled' in field_name.lower() or 'active' in field_name.lower():
        return ('bool', 'bool', 'Boolean flag')
    
    # Check for complex field patterns that need special handling
    field_lower = field_name.lower()
    if 'kamas' in field_lower or 'amount' in field_lower or 'value' in field_lower:
        decoder_hint = 'i64'
        rust_type = 'i64'
    elif 'position' in field_lower:
        if 's' in field_lower:  # positions (plural)
            rust_type = 'Vec<i64>'
            decoder_hint = 'csv'
        else:
            rust_type = 'i64'
            decoder_hint = 'i64'
    elif 'ids' in field_lower:
        rust_type = 'Vec<i64>'
        decoder_hint = 'csv'
    elif 'name' in field_lower or 'label' in field_lower or 'title' in field_lower:
        rust_type = 'String'
        decoder_hint = 'string'
    elif 'message' in field_lower or 'text' in field_lower or 'content' in field_lower:
        rust_type = 'String'
        decoder_hint = 'string'
    else:
        # Use base mappings or default to String
        if go_type in base_mappings:
            rust_type, decoder_hint, comment = base_mappings[go_type]
        else:
            rust_type = 'String'
            decoder_hint = 'string'
            comment = f'Unknown type {go_type}'
    
    return rust_type, decoder_hint, comment

def process_struct(struct_data: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single struct and create Rust mapping"""
    struct_name = struct_data['struct_name']
    fields = struct_data['fields']
    
    processed_fields = []
    for field in fields:
        go_type = field['go_type']
        is_pointer = field['is_pointer']
        is_slice = field['is_slice']
        field_name = field['name']
        
        # Get Rust type mapping
        rust_type, decoder_hint, comment = get_rust_type(
            go_type, is_pointer, is_slice, field_name, overrides
        )
        
        # Convert field name to snake_case
        rust_field_name = camel_to_snake(field_name)
        
        processed_field = {
            'name_go': field_name,
            'name_rust': rust_field_name,
            'go_type': go_type,
            'rust_type': rust_type,
            'is_pointer': is_pointer,
            'is_slice': is_slice,
            'decoder_hint': decoder_hint,
            'comment': comment
        }
        
        processed_fields.append(processed_field)
    
    return {
        'struct_name': struct_name,
        'rust_struct_name': struct_name,  # Keep same name for now
        'fields': processed_fields,
        'package': struct_data['package'],
        'file_path': struct_data['file_path']
    }

def main():
    """Main execution function"""
    # Load schema index
    schema_path = Path("schema_index.json")
    if not schema_path.exists():
        print("Error: schema_index.json not found. Run go_schema_index.py first.")
        return
    
    with open(schema_path, 'r') as f:
        schema_data = json.load(f)
    
    print(f"Processing {schema_data['total_structs']} structs...")
    
    # Load overrides
    overrides = load_overrides()
    if overrides:
        print(f"Loaded {len(overrides)} field overrides")
    
    # Process all structs
    processed_structs = {}
    for struct_name, struct_data in schema_data['structs'].items():
        processed_struct = process_struct(struct_data, overrides)
        processed_structs[struct_name] = processed_struct
    
    # Create output
    output = {
        'generated_at': '2025-11-07T01:25:54Z',
        'total_structs': len(processed_structs),
        'overrides_used': len(overrides),
        'structs': processed_structs
    }
    
    # Write output
    output_path = "schema_rust_map.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== Mapping Summary ===")
    print(f"Total structs processed: {len(processed_structs)}")
    print(f"Output written to: {output_path}")
    
    # Count decoder hints
    hint_counts = {}
    for struct in processed_structs.values():
        for field in struct['fields']:
            hint = field['decoder_hint']
            hint_counts[hint] = hint_counts.get(hint, 0) + 1
    
    print("\nDecoder hints used:")
    for hint, count in sorted(hint_counts.items()):
        print(f"  {hint}: {count}")
    
    return output

if __name__ == "__main__":
    main()