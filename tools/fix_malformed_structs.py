#!/usr/bin/env python3
"""
Final fix for malformed struct initialization - handle the exact pattern seen in errors
"""

import re
from pathlib import Path

def fix_malformed_struct_initialization(content: str) -> str:
    """Fix the specific malformed struct initialization patterns"""
    
    # Fix the exact pattern: field_name},; -> field_name},
    content = re.sub(r'(\w+),\s*\};,', r'\1},', content)
    
    # Fix the exact pattern: field_name},; -> field_name},
    content = re.sub(r'(\w+),\s*\};', r'\1},', content)
    
    # Ensure we have proper struct formatting
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Look for the malformed pattern
        if re.search(r'\w+},\s*\};,?', line) and '    let result =' not in line:
            # This is a malformed struct field line
            # Extract the field name and fix it
            field_match = re.search(r'(\w+),?\s*\};,?', line)
            if field_match:
                field_name = field_match.group(1)
                # Replace with properly formatted line
                line = f'        {field_name},'
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_malformed_struct_initialization(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed malformed struct: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all files with malformed struct initialization"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for the specific malformed pattern
            if '},;' in content or '},;,' in content:
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with malformed struct initialization")

if __name__ == "__main__":
    main()