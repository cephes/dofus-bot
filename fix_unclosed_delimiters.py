#!/usr/bin/env python3
"""Fix all files with unclosed delimiters by adding missing return statements"""

import os
import re
from pathlib import Path

def fix_unclosed_delimiter_file(file_path):
    """Fix unclosed delimiter in a single Rust file by adding missing return statements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to find the problematic if-else blocks
        # Look for if p.is_empty() { Ok(StructName {}) } else { // comment only }
        pattern = r'(\s+if p\.is_empty\(\) \{\s*Ok\(([^}]+)\{\}\)\s*\})\s+else \{\s*//[^}]+\s*\}\s*\}'
        
        def replace_else(match):
            struct_name = match.group(2).strip()
            # Extract just the struct name from the full type path
            if ' ' in struct_name:
                struct_name = struct_name.split()[-1]
            
            return f'{match.group(1)} else {{        // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n        // return Err(format!("expected empty payload for {struct_name}, got: {{}}", p));\n        Ok({struct_name} {{}})\n    }}'
        
        content = re.sub(pattern, replace_else, content, flags=re.MULTILINE | re.DOTALL)
        
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
        if fix_unclosed_delimiter_file(rust_file):
            print(f"Fixed: {rust_file}")
            fixed_count += 1
    
    print(f"Fixed unclosed delimiters in {fixed_count}/{total_files} files")

if __name__ == "__main__":
    main()