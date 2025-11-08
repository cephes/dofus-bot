#!/usr/bin/env python3
"""
Fix the specific pattern: amount},; -> amount,
"""

import re
from pathlib import Path

def fix_specific_pattern(content: str) -> str:
    """Fix the specific pattern amount},; -> amount,"""
    # Fix the specific pattern seen in the error: amount},; -> amount,
    content = content.replace('amount},;', 'amount,')
    content = content.replace('},;', '},')
    content = content.replace('},;', '},')
    
    # Also fix any other similar patterns
    content = re.sub(r'(\w+),\s*\};,', r'\1,', content)
    
    return content

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_specific_pattern(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all files with the specific malformed pattern"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for the specific pattern
            if '},;' in content:
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with specific malformed pattern")

if __name__ == "__main__":
    main()