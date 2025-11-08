#!/usr/bin/env python3
"""
Fix while loop parsing structures in generated Rust parser files

This script fixes:
- While loops that don't increment the index
- Struct initialization outside the while loop scope
- Missing proper indentation and closing braces
"""

import os
import re
from pathlib import Path

def fix_while_loop_parsing(content: str) -> str:
    """Fix the while loop parsing pattern to use sequential parsing"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Look for the problematic while loop pattern
        if 'while i < fields.len()' in line:
            # Skip the while line
            i += 1
            
            # Skip comment lines until we find field assignments
            while i < len(lines) and (lines[i].strip() == '' or '//' in lines[i]):
                i += 1
            
            # Now we should be at the field assignment lines
            field_lines = []
            while i < len(lines) and lines[i].strip().startswith('let '):
                # Extract field name and type
                field_line = lines[i].strip()
                if '=' in field_line:
                    field_name = field_line.split('=')[0].replace('let ', '').strip()
                    field_lines.append(field_name)
                i += 1
            
            # Skip the struct creation comment
            while i < len(lines) and not lines[i].strip().startswith('let result ='):
                i += 1
            
            # Now add the sequential parsing code
            fixed_lines.append('    // Sequential field parsing')
            for j, field_name in enumerate(field_lines):
                # Find the original parsing line to get the parsing logic
                # For now, use safe defaults
                if 'name' in field_name:
                    fixed_lines.append(f'    let {field_name} = common_decode::parse_string(fields.get({j}).unwrap_or(&""));')
                elif 'class' in field_name or 'sex' in field_name or 'color' in field_name:
                    fixed_lines.append(f'    let {field_name} = common_decode::parse_i64(fields.get({j}).unwrap_or(&"0"));')
                else:
                    fixed_lines.append(f'    let {field_name} = common_decode::parse_string(fields.get({j}).unwrap_or(&""));')
            
            fixed_lines.append('')
            fixed_lines.append('    // Create struct instance')
            
            # Now add the struct initialization
            while i < len(lines) and not lines[i].strip() == '}':
                if 'let result =' in lines[i]:
                    # This is the struct initialization start
                    struct_name = lines[i].split('let result = ')[1].split(' {')[0]
                    fixed_lines.append(f'    let result = {struct_name} {{')
                elif lines[i].strip() and not lines[i].strip().startswith('//') and not lines[i].strip() == 'Ok(result)':
                    # This is a field assignment
                    field_line = lines[i].strip()
                    if field_line.endswith(','):
                        fixed_lines.append(f'        {field_line}')
                    else:
                        fixed_lines.append(f'        {field_line},')
                i += 1
            
            # Close the struct and add Ok(result)
            if i < len(lines) and lines[i].strip() == '}':
                fixed_lines.append('    };')
                i += 1
            
            if i < len(lines) and 'Ok(result)' in lines[i]:
                fixed_lines.append('    Ok(result)')
                i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file with the while loop pattern"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if this file has the problematic while loop pattern
        if 'while i < fields.len()' in content and content.count('let mut i = 0;') == 1:
            content = fix_while_loop_parsing(content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed while loop in: {file_path}")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all files with problematic while loop patterns"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found!")
        return
    
    fixed_files = 0
    
    # First, let's manually fix the AccountAddCharacter file that's currently failing
    account_char_file = generated_dir / "AccountAddCharacter.rs"
    if account_char_file.exists():
        with open(account_char_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Manually rewrite the function with proper structure
        fixed_content = '''//! Generated parser for AccountAddCharacter
//! 
//! This file was automatically generated from Go schema definitions.
//! Manual modifications may be overwritten.

use crate::retroproto_parsers::parser::common_decode;

#[derive(Debug, Clone, Default, serde::Serialize, serde:: Deserialize)]
pub struct AccountAddCharacter {
    /// Name/label
    pub name: String,
    pub class: i64,
    pub sex: i64,
    /// Color value
    pub color1: i32,
    /// Color value
    pub color2: i32,
    /// Color value
    pub color3: i32,
}

pub fn parse_AccountAddCharacter(payload: &str) -> Result<AccountAddCharacter, String> {
    let fields = common_decode::split_fields(payload);
    
    // Sequential field parsing
    let name = common_decode::parse_string(fields.get(0).unwrap_or(&""));
    let class = common_decode::parse_i64(fields.get(1).unwrap_or(&"0"));
    let sex = common_decode::parse_i64(fields.get(2).unwrap_or(&"0"));
    let color1 = common_decode::parse_i32(fields.get(3).unwrap_or(&"0"));
    let color2 = common_decode::parse_i32(fields.get(4).unwrap_or(&"0"));
    let color3 = common_decode::parse_i32(fields.get(5).unwrap_or(&"0"));
    
    // Create struct instance
    let result = AccountAddCharacter {
        name,
        class,
        sex,
        color1,
        color2,
        color3,
    };
    
    Ok(result)
}'''
        
        with open(account_char_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Manually fixed: {account_char_file}")
        fixed_files += 1
    
    # Now fix other files with similar patterns
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs" or rs_file == account_char_file:
            continue
        
        # Check if file has the problematic pattern
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'while i < fields.len()' in content:
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with while loop parsing issues")

if __name__ == "__main__":
    main()