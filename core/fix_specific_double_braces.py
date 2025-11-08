#!/usr/bin/env python3
"""
Fix the specific double brace pattern in Ok() statements.
"""

import os
import re
from pathlib import Path

def fix_specific_double_braces(file_path):
    """Fix the specific double brace pattern: Ok(...) }}) -> Ok(...) }"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Ok(...) followed by }} at the end
        content = re.sub(
            r'Ok\(([^)]*)\}\}\s*\)',
            r'Ok(\1) }',
            content
        )
        
        # Fix Ok(...})}) pattern (with closing paren)
        content = re.sub(
            r'Ok\(([^)]*)\}\}\)\s*',
            r'Ok(\1) }',
            content
        )
        
        # More aggressive pattern - just remove one of the double braces
        content = re.sub(
            r'Ok\(([^)]*)\}\}\)\s*',
            r'Ok(\1) }',
            content
        )
        
        # If content changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix double braces in all generated parser files."""
    generated_dir = Path('src/retroproto_parsers/generated')
    
    if not generated_dir.exists():
        print(f"Generated directory {generated_dir} does not exist")
        return
    
    # Get all .rs files in generated directory
    rs_files = list(generated_dir.glob('*.rs'))
    
    if not rs_files:
        print("No .rs files found in generated directory")
        return
    
    print(f"Found {len(rs_files)} .rs files to process")
    
    fixed_files = 0
    for file_path in rs_files:
        if fix_specific_double_braces(file_path):
            print(f"Fixed specific double braces in: {file_path}")
            fixed_files += 1
    
    print(f"\nSpecific double brace fixes applied to {fixed_files} files")

if __name__ == '__main__':
    main()