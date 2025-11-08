#!/usr/bin/env python3
"""
Systematic Fix for Parser Compilation Issues

This script fixes the 291 compilation errors in the generated parser files by:
1. Adding missing variable declarations (i, j, etc.) in parse functions
2. Fixing field name access issues (reserved keywords like 'type' → 'r#type')
3. Replacing undefined type references (typ → String) 
4. Fixing prefix issues in reserved keyword fields
5. Removing unused variable warnings
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

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
        # Look for patterns like fields.get(i) but no let mut i = 0;
        if re.search(r'fields\.get\(i\)', content) and 'let mut i' not in content:
            # Add variable declaration at the start of function body
            # Find the function body start
            func_pattern = r'(pub fn parse_\w+\(payload: &str\) -> Result<\w+, String> \{)'
            match = re.search(func_pattern, content)
            if match:
                insertion_point = match.end()
                content = content[:insertion_point] + "\n    let mut i = 0;" + content[insertion_point:]
                changes_made.append("Added missing 'let mut i = 0;'")
        
        # Fix 2: Handle reserved keywords in field names (type -> r#type)
        # Look for field declarations and struct access
        reserved_keywords = ['type', 'match', 'if', 'else', 'for', 'while', 'fn', 'let', 'struct', 'enum', 'impl', 'pub', 'use', 'mod', 'crate']
        
        for keyword in reserved_keywords:
            # Fix struct field declarations
            pattern = rf'(\s*pub {keyword}:)'
            if re.search(pattern, content):
                content = re.sub(pattern, rf'\1r#{keyword}:', content)
                changes_made.append(f"Fixed reserved keyword in field declaration: {keyword}")
            
            # Fix struct initialization
            pattern = rf'({keyword}:)'
            if re.search(pattern, content) and not re.search(rf'(\s*pub\s+r#{keyword}:)', content):
                content = re.sub(pattern, rf'r#\1', content)
                changes_made.append(f"Fixed reserved keyword in struct init: {keyword}")
        
        # Fix 3: Replace undefined type references (typ -> String)
        content = re.sub(r'Vec<typ>', 'Vec<String>', content)
        content = re.sub(r'<typ>', '<String>', content)
        if '<typ>' in original_content or 'Vec<typ>' in original_content:
            changes_made.append("Replaced undefined 'typ' with 'String'")
        
        # Fix 4: Fix field variable references (missing i increment)
        # Find all fields.get(i) calls and add i increment
        fields_get_pattern = r'(let \w+ = common_decode::[^;]+fields\.get\(i\)\.unwrap_or\([^)]+\)\);)'
        def add_i_increment(match):
            return match.group(1) + "\n        i += 1;"
        new_content = re.sub(fields_get_pattern, add_i_increment, content)
        if new_content != content:
            content = new_content
            changes_made.append("Added i += 1 after each field access")
        
        # Fix 5: Remove unused variable warnings for fields
        content = re.sub(r'let fields = common_decode::split_fields\(payload\);', 
                        'let _fields = common_decode::split_fields(payload);', content)
        if 'let fields' in original_content and 'let _fields' in content:
            changes_made.append("Renamed 'fields' to '_fields' to remove unused warning")
        
        # Fix 6: Fix import paths if needed
        if 'use crate::retroproto_parsers::parser::common_decode;' not in content:
            content = content.replace('use crate::retroproto_parsers::parser::common_decode;',
                                    'use crate::retroproto_parsers::parser::common_decode;')
        
        # Fix 7: Add missing field parsing in some files
        # Look for parse functions that have struct fields but no parsing code
        struct_fields = re.findall(r'pub (\w+): (\w+),', content)
        parsing_lines = re.findall(r'let (\w+) = ', content)
        
        for field_name, field_type in struct_fields:
            if field_name not in parsing_lines and field_name not in ['action_type', 'action_movement']:  # Skip fields already handled
                # Add field parsing
                if field_type in ['String', 'str']:
                    parse_code = f'        let {field_name} = common_decode::parse_string(fields.get(i).unwrap_or(&""));'
                elif field_type in ['i64']:
                    parse_code = f'        let {field_name} = common_decode::parse_i64(fields.get(i).unwrap_or(&"0"));'
                elif field_type in ['i32']:
                    parse_code = f'        let {field_name} = common_decode::parse_i32(fields.get(i).unwrap_or(&"0"));'
                elif field_type in ['bool']:
                    parse_code = f'        let {field_name} = common_decode::parse_bool(fields.get(i).unwrap_or(&"0"));'
                else:
                    parse_code = f'        let {field_name} = common_decode::parse_string(fields.get(i).unwrap_or(&""));'
                
                # Find the right place to insert (before struct creation)
                struct_creation_pattern = r'// Create struct instance\s*let result ='
                if re.search(struct_creation_pattern, content):
                    content = re.sub(struct_creation_pattern, 
                                   parse_code + '\n    \g<0>', content)
                    changes_made.append(f"Added missing field parsing: {field_name}")
        
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
    print("🔧 Starting Parser Compilation Fix...")
    print("=" * 60)
    
    parser_files = find_parser_files()
    print(f"Found {len(parser_files)} parser files to fix")
    
    success_count = 0
    fixed_count = 0
    error_count = 0
    
    for file_path in parser_files:
        print(f"\n📄 Processing: {file_path.relative_to(Path('.'))}")
        
        success, message = fix_parser_file(file_path)
        
        if success:
            if "No changes needed" not in message:
                fixed_count += 1
                print(f"✅ FIXED: {message}")
            else:
                print(f"ℹ️  {message}")
            success_count += 1
        else:
            error_count += 1
            print(f"❌ ERROR: {message}")
    
    print("\n" + "=" * 60)
    print("📊 COMPILATION FIX SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(parser_files)}")
    print(f"Successfully processed: {success_count}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files with errors: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 Successfully fixed {fixed_count} parser files!")
        print("Run 'cd core && cargo check' to verify compilation")
    else:
        print(f"\n⚠️  No files required fixing")
    
    return fixed_count

if __name__ == "__main__":
    main()