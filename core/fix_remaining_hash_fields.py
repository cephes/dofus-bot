#!/usr/bin/env python3
"""
Fix remaining field names with # symbols that weren't caught by the previous fix.
Targeting specific patterns like action_r#type, item_r#type, etc.
"""

import os
import re
import glob
from pathlib import Path

def fix_hash_field_names(content):
    """Fix field names that contain # symbols"""
    
    # Pattern to match field names with # in struct initialization
    # Looking for patterns like: action_r#type, item_r#type, etc.
    patterns = [
        (r'(\w+)#(\w+)', r'\1\2'),  # Remove # from field names
        (r'(\w+_)#(\w+)', r'\1\2'),  # Specifically handle cases like action_r#type -> action_rtype
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def main():
    """Fix all remaining # symbols in field names"""
    base_dir = Path("src/retroproto_parsers/generated")
    
    # Count files processed
    processed = 0
    errors = []
    
    # Find all .rs files
    rs_files = list(base_dir.rglob("*.rs"))
    
    print(f"Processing {len(rs_files)} Rust files...")
    
    for file_path in rs_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply fixes
            fixed_content = fix_hash_field_names(original_content)
            
            # Check if changes were made
            if fixed_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                processed += 1
                print(f"Fixed: {file_path.relative_to(base_dir)}")
        
        except Exception as e:
            errors.append(f"Error processing {file_path}: {e}")
    
    print(f"\nCompleted!")
    print(f"Files fixed: {processed}")
    print(f"Total files: {len(rs_files)}")
    
    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  {error}")
    
    return processed

if __name__ == "__main__":
    main()