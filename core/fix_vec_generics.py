#!/usr/bin/env python3
"""
Fix missing Vec generic parameters in generated Rust files.
Converts `Vec` to `Vec<String>` for string arrays and `Vec<i64>` for numeric arrays.
"""

import os
import re
import glob

def fix_vec_generics_in_file(file_path):
    """Fix Vec generic parameters in a single Rust file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to find Vec without generic parameter
        # Look for lines with just "Vec" followed by comma, semicolon, or end of line
        patterns = [
            # pub field: Vec,
            (r'(\w+:\s+)Vec(\s*,|\s*;|\s*)$', r'\1Vec<String>\2'),
            # pub field: Vec
            (r'(\w+:\s+)Vec(\s*)$', r'\1Vec<String>\2'),
            # Vec
            (r'(\s+)Vec(\s*,|\s*;|\s*)$', r'\1Vec<String>\2'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Special case: if the field is clearly numeric (contains 'id', 'count', 'number', etc.)
        # Use Vec<i64> instead
        numeric_patterns = [
            (r'(\w*(?:id|count|number|index|position|size|length|amount|value|level)\w*:\s+)Vec(\s*,|\s*;|\s*)$', r'\1Vec<i64>\2'),
            (r'(\w*(?:id|count|number|index|position|size|length|amount|value|level)\w*:\s+)Vec(\s*)$', r'\1Vec<i64>\2'),
        ]
        
        for pattern, replacement in numeric_patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Vec generics in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix Vec generics in all generated Rust files."""
    generated_dir = "src/retroproto_parsers/generated"
    
    if not os.path.exists(generated_dir):
        print(f"Directory {generated_dir} not found!")
        return
    
    # Get all .rs files in the generated directory
    rust_files = glob.glob(os.path.join(generated_dir, "*.rs"))
    
    print(f"Found {len(rust_files)} Rust files to check...")
    
    fixed_count = 0
    for file_path in rust_files:
        if fix_vec_generics_in_file(file_path):
            fixed_count += 1
    
    print(f"Fixed Vec generics in {fixed_count} files")

if __name__ == "__main__":
    main()