#!/usr/bin/env python3
"""
Final comprehensive syntax fix for generated Rust parser files

This script fixes:
- Double semicolons (},; -> };)
- Malformed struct initialization
- Missing field parsing logic
- Proper indentation and formatting
"""

import os
import re
from pathlib import Path

def fix_struct_initialization_syntax(content: str) -> str:
    """Fix struct initialization syntax issues"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Fix double semicolon patterns
        line = line.replace('},;', '};')
        
        # Fix struct initialization lines
        if '};,' in line:
            line = line.replace('};,', '},')
        
        # Look for struct field assignments and fix them
        if 'let result =' in line and '{' in line:
            # This is the start of struct initialization
            fixed_lines.append(line)
            i += 1
            
            # Collect all struct field lines
            while i < len(lines) and not lines[i].strip() == '};':
                current_line = lines[i].strip()
                if current_line:
                    # Fix any field line issues
                    if current_line.endswith(','):
                        # Already has comma, make sure it's properly formatted
                        fixed_lines.append(f'        {current_line}')
                    elif current_line == '}' or current_line == '};':
                        # This shouldn't happen here, skip it
                        pass
                    else:
                        # No comma, add one
                        if ':' in current_line:
                            fixed_lines.append(f'        {current_line},')
                        else:
                            # This might be a malformed line, fix it
                            fixed_lines.append(f'        {current_line},')
                i += 1
            
            # Add the closing brace
            if i < len(lines) and lines[i].strip() == '};':
                fixed_lines.append('    };')
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def fix_field_parsing_logic(content: str, struct_name: str) -> str:
    """Fix the field parsing logic to be sequential"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    # Find the struct fields to determine parsing order
    struct_fields = []
    in_struct = False
    
    for line in lines:
        if f'pub struct {struct_name} {{' in line:
            in_struct = True
        elif in_struct and '}' in line:
            in_struct = False
        elif in_struct and 'pub ' in line and ':' in line:
            # Extract field name
            field_part = line.split(':')[0].replace('pub', '').strip()
            struct_fields.append(field_part)
    
    # Now fix the parsing function
    while i < len(lines):
        line = lines[i]
        
        # Skip the old sequential parsing comment and field assignments
        if '// Sequential field parsing' in line:
            # Replace with new sequential parsing
            fixed_lines.append('    // Sequential field parsing')
            i += 1
            
            # Add field parsing for each struct field
            for j, field_name in enumerate(struct_fields):
                if field_name in ['name', 'pseudo', 'reason', 'value', 'level', 'lang', 'position', 'port', 'id', 'extra', 'authorized', 'queue_id', 'restrictions', 'crypto_method', 'secret_answer', 'servers_characters', 'color1', 'color2', 'color3', 'items', 'characters']:
                    if 'color' in field_name:
                        fixed_lines.append(f'    let {field_name} = common_decode::parse_i32(fields.get({j}).unwrap_or(&"0"));')
                    else:
                        fixed_lines.append(f'    let {field_name} = common_decode::parse_string(fields.get({j}).unwrap_or(&""));')
                else:
                    # Default to string parsing
                    fixed_lines.append(f'    let {field_name} = common_decode::parse_string(fields.get({j}).unwrap_or(&""));')
            
            # Skip the old field assignment lines
            while i < len(lines) and not (lines[i].strip().startswith('// Create struct instance') or lines[i].strip() == 'let result ='):
                i += 1
            if i < len(lines):
                fixed_lines.append(lines[i])  # Add the comment
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def extract_struct_name_from_file(file_path: Path) -> str:
    """Extract the struct name from the file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the struct definition
        for line in content.split('\n'):
            if 'pub struct ' in line and '{' in line:
                struct_name = line.split('pub struct ')[1].split(' {')[0].strip()
                return struct_name
    except:
        pass
    return None

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file comprehensively"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Extract struct name
        struct_name = extract_struct_name_from_file(file_path)
        
        # Apply comprehensive fixes
        content = fix_struct_initialization_syntax(content)
        if struct_name:
            content = fix_field_parsing_logic(content, struct_name)
        
        # Final cleanup for any remaining issues
        content = content.replace('},;,', '},')
        content = content.replace('},;', '};')
        
        # Ensure proper struct initialization format
        content = re.sub(r'(\w+,\s*\});,', r'\1};', content)
        content = re.sub(r'(\w+,\s*\});', r'\1};', content)
        
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
    """Fix all generated parser files with comprehensive syntax fixes"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found!")
        return
    
    fixed_files = 0
    
    # Find all .rs files that need fixing
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has syntax issues
            if ('},;' in content or '};,' in content or 
                'let result =' in content and '    };' not in content):
                
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with comprehensive syntax fixes")

if __name__ == "__main__":
    main()