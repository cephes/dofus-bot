#!/usr/bin/env python3
"""
Simple script to fix Ok() expressions missing closing parentheses and semicolons.
"""

import os
import re
from pathlib import Path

def fix_ok_expressions(file_path):
    """Fix Ok() expressions missing closing parentheses and semicolons."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Ok(...} -> Ok(...});
        content = re.sub(r'Ok\([^)]*\)\s*\}\s*$', r'Ok(\1);', content, flags=re.MULTILINE)
        
        # Fix Ok(...unwrap_or_default() } -> Ok(...unwrap_or_default());
        content = re.sub(r'unwrap_or_default\(\)\s*\}\s*$', r'unwrap_or_default());', content, flags=re.MULTILINE)
        
        # Fix lines that have Ok( and end with } but not });
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Ok(' in line and line.strip().endswith('}') and not line.strip().endswith('});'):
                # Replace trailing } with });
                line = line.rstrip('}') + '});'
                lines[i] = line
        
        content = '\n'.join(lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix Ok() expressions in all generated parser files."""
    generated_dir = Path('src/retroproto_parsers/generated')
    
    if not generated_dir.exists():
        print(f"Generated directory {generated_dir} does not exist")
        return
    
    rs_files = list(generated_dir.glob('*.rs'))
    
    if not rs_files:
        print("No .rs files found in generated directory")
        return
    
    print(f"Found {len(rs_files)} .rs files to process")
    
    fixed_files = 0
    for file_path in rs_files:
        if fix_ok_expressions(file_path):
            print(f"Fixed Ok() expressions in: {file_path}")
            fixed_files += 1
    
    print(f"\nOk() expression fixes applied to {fixed_files} files")

if __name__ == '__main__':
    main()