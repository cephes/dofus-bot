#!/usr/bin/env python3
"""Fix extra parentheses and braces in generated Rust files"""

import os
import re
from pathlib import Path

def fix_delimiters_in_file(file_path):
    """Fix delimiter issues in a single Rust file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common delimiter patterns
        # Remove extra closing parentheses after struct literals
        content = re.sub(r'\}\}\)', '})', content)
        content = re.sub(r'\}\}\)', '})', content)
        
        # Fix specific patterns like Ok(Struct { field: value }})
        content = re.sub(r'Ok\(\s*(\w+\s*\{[^}]*\})\s*\}\)\s*\)', r'Ok(\1)', content)
        content = re.sub(r'Ok\(\s*(\w+\s*\{[^}]*\})\s*\}\s*\)', r'Ok(\1)', content)
        
        # Fix json! macro calls
        content = re.sub(r'json!\(\s*([^)]*)\s*\}\s*\)', r'json!(\1) }', content)
        
        # Fix any remaining double delimiters
        content = re.sub(r'\}\}\s*\)', '})', content)
        content = re.sub(r'\)\)\s*\)', '))', content)
        
        # Fix missing closing braces
        content = re.sub(r'pub fn \w+.*?\([^)]*\) -> .*? \{([^}]*)\}\s*\)\s*$', r'pub fn \1 -> \2 { \3 })', content, flags=re.MULTILINE | re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Find all generated Rust files
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print(f"Directory {generated_dir} does not exist")
        return
    
    fixed_count = 0
    total_files = 0
    
    # Process all .rs files recursively
    for rust_file in generated_dir.rglob("*.rs"):
        total_files += 1
        if fix_delimiters_in_file(rust_file):
            print(f"Fixed: {rust_file}")
            fixed_count += 1
    
    print(f"Fixed delimiters in {fixed_count}/{total_files} files")

if __name__ == "__main__":
    main()