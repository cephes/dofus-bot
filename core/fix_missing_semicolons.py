#!/usr/bin/env python3
"""
Fix missing semicolons and extra braces in Ok() statements across all generated parser files.
"""

import os
import re
from pathlib import Path

def fix_missing_semicolons_and_braces(file_path):
    """Fix missing semicolons and extra braces in Ok() statements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix missing semicolon at end of Ok() expressions
        # Pattern: Ok(...) followed by closing brace on next line
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\)\s*(\n\s*})',
            r'Ok(\1);\2',
            content
        )
        
        # Fix cases where Ok() is on same line as closing brace but missing semicolon
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\}\s*\)',
            r'Ok(\1);',
            content
        )
        
        # Fix extra closing braces in Ok() expressions
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\}\)\s*',
            r'Ok(\1);',
            content
        )
        
        # Fix Ok() followed directly by closing brace without semicolon
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\)\s*(\n\s*}\s*\n)',
            r'Ok(\1);\2',
            content
        )
        
        # Fix Ok() at end of function without semicolon
        content = re.sub(
            r'Ok\(\s*([^)]*)\s*\}\)\s*$',
            r'Ok(\1);',
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
    """Fix syntax issues in all generated parser files."""
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
        if fix_missing_semicolons_and_braces(file_path):
            print(f"Fixed syntax in: {file_path}")
            fixed_files += 1
    
    print(f"\nSyntax fixes applied to {fixed_files} files")

if __name__ == '__main__':
    main()