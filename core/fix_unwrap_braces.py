#!/usr/bin/env python3
"""
Fix the specific pattern: unwrap_or_default() }}) -> unwrap_or_default() }
"""

import os
import re
from pathlib import Path

def fix_unwrap_braces(file_path):
    """Fix the specific pattern: unwrap_or_default() }}) -> unwrap_or_default() }"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the specific pattern: unwrap_or_default() }} at end of Ok() expression
        content = re.sub(
            r'unwrap_or_default\(\)\s*\}\}\s*\)',
            r'unwrap_or_default() }',
            content
        )
        
        # Fix any case where there are extra closing braces at the end of Ok() expressions
        content = re.sub(
            r'Ok\([^)]*\)\s*\}\}\s*\)',
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
    """Fix unwrap_or_default braces in all generated parser files."""
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
        if fix_unwrap_braces(file_path):
            print(f"Fixed unwrap braces in: {file_path}")
            fixed_files += 1
    
    print(f"\nUnwrap brace fixes applied to {fixed_files} files")

if __name__ == '__main__':
    main()