#!/usr/bin/env python3
"""
Go Schema Indexer - Extract Go structs from retroproto schemas

Recursively parses third_party/retroproto/msgsvr + msgcli directories
to extract all message structs with their fields and metadata.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_struct_from_go_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract struct definition from a Go file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
    # Find package name
    package_match = re.search(r'package\s+(\w+)', content)
    package_name = package_match.group(1) if package_match else "unknown"
    
    # Find struct definition
    # Match type StructName struct { ... }
    struct_pattern = r'type\s+(\w+)\s+struct\s*\{([^}]*)\}'
    struct_match = re.search(struct_pattern, content, re.DOTALL)
    
    if not struct_match:
        return None
    
    struct_name = struct_match.group(1)
    struct_body = struct_match.group(2)
    
    # Extract fields
    fields = []
    field_lines = struct_body.strip().split('\n')
    
    for line in field_lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue
            
        # Match field: `Name Type` or `Name *Type` or `Name []Type`
        field_match = re.match(r'(\w+)\s+(\*?)(\[\])?(\w+|`[^`]*`)', line)
        if field_match:
            field_name = field_match.group(1)
            is_pointer = bool(field_match.group(2))
            is_slice = bool(field_match.group(3))
            field_type = field_match.group(4)
            
            # Remove backticks from string types
            if field_type.startswith('`') and field_type.endswith('`'):
                field_type = field_type[1:-1]
            
            fields.append({
                "name": field_name,
                "go_type": field_type,
                "is_pointer": is_pointer,
                "is_slice": is_slice,
                "full_type": f"{'*' if is_pointer else ''}{'[]' if is_slice else ''}{field_type}"
            })
    
    return {
        "package": package_name,
        "file_path": str(file_path),
        "struct_name": struct_name,
        "fields": fields,
        "line_count": len(content.split('\n'))
    }

def should_process_file(file_path: Path) -> bool:
    """Check if file should be processed"""
    # Skip certain files
    skip_patterns = ['_test.go', 'main.go', 'cmd/']
    for pattern in skip_patterns:
        if pattern in str(file_path):
            return False
    
    # Only process .go files in msgcli and msgsvr directories
    if not file_path.suffix == '.go':
        return False
        
    parent_dirs = [p.name for p in file_path.parents]
    return 'msgcli' in parent_dirs or 'msgsvr' in parent_dirs

def scan_directory_for_structs(root_path: Path) -> List[Dict[str, Any]]:
    """Recursively scan directory for Go struct definitions"""
    structs = []
    
    for file_path in root_path.rglob('*.go'):
        if should_process_file(file_path):
            struct_def = extract_struct_from_go_file(file_path)
            if struct_def:
                structs.append(struct_def)
                print(f"Found struct {struct_def['struct_name']} in {file_path}")
    
    return structs

def main():
    """Main execution function"""
    retroproto_root = Path("third_party/retroproto")
    
    if not retroproto_root.exists():
        print(f"Error: {retroproto_root} does not exist")
        return
    
    print(f"Scanning Go structs in {retroproto_root}")
    
    all_structs = []
    
    # Scan msgcli and msgsvr directories
    for subdir in ['msgcli', 'msgsvr']:
        dir_path = retroproto_root / subdir
        if dir_path.exists():
            print(f"\nScanning {subdir} directory...")
            structs = scan_directory_for_structs(dir_path)
            all_structs.extend(structs)
    
    # Create output
    output = {
        "scanned_at": "2025-11-07T01:25:18Z",
        "total_structs": len(all_structs),
        "structs": {}
    }
    
    # Group by struct name
    for struct in all_structs:
        struct_name = struct['struct_name']
        output["structs"][struct_name] = struct
    
    # Write JSON output
    output_path = "schema_index.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== Summary ===")
    print(f"Total structs found: {len(all_structs)}")
    print(f"Output written to: {output_path}")
    
    # Show breakdown by package
    package_counts = {}
    for struct in all_structs:
        package = struct['package']
        package_counts[package] = package_counts.get(package, 0) + 1
    
    print("\nStructs by package:")
    for package, count in sorted(package_counts.items()):
        print(f"  {package}: {count}")
    
    return output

if __name__ == "__main__":
    main()