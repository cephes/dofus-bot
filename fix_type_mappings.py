#!/usr/bin/env python3
"""
Fix type mapping issues in generated Rust files
"""
import os
from pathlib import Path

def fix_type_mappings(file_path):
    """Fix type mapping issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix position field mappings that are getting wrong types
        # Replace parse_string with parse_i64 for position fields
        content = content.replace(
            'let position = common_decode::parse_string_list(fields.get(i).unwrap_or(&""));',
            'let position = common_decode::parse_i64_list(fields.get(i).unwrap_or(&""));'
        )
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed type mapping: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main execution function"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found")
        return
    
    fixed_count = 0
    for file_path in generated_dir.rglob("*.rs"):
        if file_path.name != "mod.rs":
            if fix_type_mappings(file_path):
                fixed_count += 1
    
    print(f"Fixed type mapping issues in {fixed_count} files")

if __name__ == "__main__":
    main()