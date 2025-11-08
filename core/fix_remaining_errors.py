#!/usr/bin/env python3
"""
Final comprehensive fix for remaining compilation errors.
"""

import os
import re
import glob

def fix_field_name_mismatches(file_path):
    """Fix field name mismatches in struct initialization."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Field name fixes
        fixes = [
            # action_type -> action_r_type
            (r'\baction_type\b', 'action_r_type'),
            # action_challenge_refuse -> action_challenge_refr_use
            (r'\baction_challenge_refuse\b', 'action_challenge_refr_use'),
            # item_type -> item_r_type
            (r'\bitem_type\b', 'item_r_type'),
            # rtype -> rr_type (for Exchange structs)
            (r'\brtype\b', 'rr_type'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed field names in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_vec_types_by_context(file_path):
    """Fix Vec types based on field context and usage."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Read the file to understand field definitions
        lines = content.split('\n')
        
        # Build field type mapping from struct definition
        field_types = {}
        in_struct = False
        struct_name = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('pub struct ') and '{' in line:
                in_struct = True
                struct_name = line.split('pub struct ')[1].split(' {')[0]
            elif in_struct and ':' in line and not line.startswith('//'):
                # Parse field definition
                field_match = re.match(r'(\w+):\s*([^,}]+)', line)
                if field_match:
                    field_name = field_match.group(1)
                    field_type = field_match.group(2).strip()
                    field_types[field_name] = field_type
            
            if in_struct and '}' in line:
                in_struct = False
        
        # Now fix the struct initialization based on the field types
        for line in lines:
            # Look for struct initialization
            if ('{') in line and ('}' in line or ',') in line:
                # Extract field names and values
                field_pattern = r'(\w+):\s*(\w+),?\s*}'
                matches = re.findall(field_pattern, line)
                
                if matches:
                    new_line = line
                    for field_name, value_name in matches:
                        if field_name in field_types:
                            expected_type = field_types[field_name]
                            if 'Vec<i64>' in expected_type and 'Vec<String>' in line:
                                # Replace Vec<String> with Vec<i64> for this field
                                new_line = re.sub(
                                    rf'({field_name}:\s*)(Vec<String>)',
                                    rf'\1Vec<i64>',
                                    new_line
                                )
                            elif 'Vec<String>' in expected_type and 'Vec<i64>' in line:
                                # Replace Vec<i64> with Vec<String> for this field
                                new_line = re.sub(
                                    rf'({field_name}:\s*)(Vec<i64>)',
                                    rf'\1Vec<String>',
                                    new_line
                                )
                    
                    if new_line != line:
                        content = content.replace(line, new_line)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Vec types in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all remaining issues in generated Rust files."""
    generated_dir = "src/retroproto_parsers/generated"
    
    if not os.path.exists(generated_dir):
        print(f"Directory {generated_dir} not found!")
        return
    
    # Get all .rs files in the generated directory
    rust_files = glob.glob(os.path.join(generated_dir, "*.rs"))
    
    print(f"Found {len(rust_files)} Rust files to check...")
    
    fixed_count = 0
    for file_path in rust_files:
        # First fix field name mismatches
        if fix_field_name_mismatches(file_path):
            fixed_count += 1
        
        # Then fix Vec types
        fix_vec_types_by_context(file_path)
    
    print(f"Fixed field names in {fixed_count} files")

if __name__ == "__main__":
    main()