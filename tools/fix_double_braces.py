#!/usr/bin/env python3
"""
Final fix for brace/struct initialization issues
"""

import re
from pathlib import Path

def fix_double_braces(content: str) -> str:
    """Fix double braces and extra closing braces"""
    # Fix patterns like: amount,    }}
    content = re.sub(r',\s*\}\s*\}', '},', content)
    
    # Fix patterns like: amount,    }};
    content = re.sub(r',\s*\}\s*\};', '};', content)
    
    # Ensure proper struct initialization format
    content = re.sub(r'(\w+,\s*)\}\s*\}', r'\1}', content)
    
    return content

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_double_braces(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed braces: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all files with brace issues"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '}}' in content or '};}' in content:
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with brace issues")

if __name__ == "__main__":
    main()