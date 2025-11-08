#!/usr/bin/env python3
"""
Fix double braces in Ok() statements across all generated parser files.
"""

import os
import re
from pathlib import Path

def fix_double_braces(file_path):
    """Fix double braces in Ok() statements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix double braces in Ok() expressions: }} -> }
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\}\)',
            r'Ok(\1) }',
            content
        )
        
        # Fix cases where Ok() has extra closing brace followed by another closing brace
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\s*\}\s*\)',
            r'Ok(\1)',
            content
        )
        
        # Fix Ok() expressions ending with }} ) -> }
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\}\s*\)',
            r'Ok(\1)',
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
        if fix_double_braces(file_path):
            print(f"Fixed double braces in: {file_path}")
            fixed_files += 1
    
    print(f"\nDouble brace fixes applied to {fixed_files} files")

if __name__ == '__main__':
    main()