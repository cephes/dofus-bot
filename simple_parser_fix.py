#!/usr/bin/env python3
"""
Parser Compilation Fix - Simplified Version
Fixes the main issues in generated parser files
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def find_parser_files() -> List[Path]:
    """Find all generated parser files"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    return list(generated_dir.rglob("*.rs"))

def fix_parser_file(file_path: Path) -> Tuple[bool, str]:
    """Fix a single parser file and return (success, message)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Fix 1: Add missing variable declarations for loop counters
        if 'fields.get(i)' in content and 'let mut i' not in content:
            # Find the function body start
            func_pattern = r'(pub fn parse_\w+\(payload: &str\) -> Result<\w+, String> \{)'
            match = re.search(func_pattern, content)
            if match:
                insertion_point = match.end()
                content = content[:insertion_point] + "\n    let mut i = 0;" + content[insertion_point:]
                changes_made.append("Added missing 'let mut i = 0;'")
        
        # Fix 2: Replace undefined type references (typ -> String)
        if 'Vec<typ>' in content or '<typ>' in content:
            content = re.sub(r'Vec<typ>', 'Vec<String>', content)
            content = re.sub(r'<typ>', '<String>', content)
            changes_made.append("Replaced undefined 'typ' with 'String'")
        
        # Fix 3: Fix reserved keywords in field names
        reserved_keywords = ['type', 'match', 'if', 'else', 'for', 'while', 'fn', 'let', 'struct', 'enum', 'impl', 'pub', 'use', 'mod', 'crate']
        
        for keyword in reserved_keywords:
            # Fix struct field declarations
            pattern = rf'(\s*pub {keyword}:)'
            if re.search(pattern, content):
                content = re.sub(pattern, rf'\1r#{keyword}:', content)
                changes_made.append(f"Fixed reserved keyword in field declaration: {keyword}")
            
            # Fix struct initialization - look for r# in struct but not in field name
            pattern = rf'({keyword}:)'
            if re.search(pattern, content):
                content = re.sub(pattern, rf'r#\1', content)
                changes_made.append(f"Fixed reserved keyword in struct init: {keyword}")
        
        # Fix 4: Remove unused variable warnings for fields
        if 'let fields = common_decode::split_fields(payload);' in content:
            content = content.replace('let fields = common_decode::split_fields(payload);', 
                                    'let _fields = common_decode::split_fields(payload);')
            changes_made.append("Renamed 'fields' to '_fields' to remove unused warning")
        
        # Fix 5: Fix field references from fields to _fields
        if '_fields' in content:
            content = re.sub(r'fields\.get\(', '_fields.get(', content)
        
        # Fix 6: Add i increment after each field access
        # Find patterns like let field = ...fields.get(i).unwrap_or(...);
        def add_i_increment(match):
            return match.group(1) + "\n        i += 1;"
        
        fields_get_pattern = r'(let \w+ = common_decode::[^;]+fields\.get\(i\)\.unwrap_or\([^)]+\)\);)'
        content = re.sub(fields_get_pattern, add_i_increment, content)
        if 'i += 1' in content and 'i += 1' not in original_content:
            changes_made.append("Added i += 1 after field accesses")
        
        # Write the fixed content back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Fixed: {', '.join(changes_made)}"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Main fix function"""
    print("Starting Parser Compilation Fix...")
    print("=" * 50)
    
    parser_files = find_parser_files()
    print(f"Found {len(parser_files)} parser files to fix")
    
    success_count = 0
    fixed_count = 0
    error_count = 0
    
    for file_path in parser_files:
        print(f"Processing: {file_path.relative_to(Path('.'))}")
        
        success, message = fix_parser_file(file_path)
        
        if success:
            if "No changes needed" not in message:
                fixed_count += 1
                print(f"FIXED: {message}")
            else:
                print(f"No changes needed")
            success_count += 1
        else:
            error_count += 1
            print(f"ERROR: {message}")
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {len(parser_files)}")
    print(f"Successfully processed: {success_count}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files with errors: {error_count}")
    
    if fixed_count > 0:
        print(f"\nSuccessfully fixed {fixed_count} parser files!")
        print("Run 'cd core && cargo check' to verify compilation")
    else:
        print(f"\nNo files required fixing")
    
    return fixed_count

if __name__ == "__main__":
    main()