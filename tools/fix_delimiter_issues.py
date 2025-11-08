#!/usr/bin/env python3
"""
Fix delimiter/brace issues in generated Rust parser files

This script fixes:
- Missing closing braces in struct initializations
- Extra/missing commas
- Indentation issues
"""

import os
import re
from pathlib import Path

def fix_struct_constructor_syntax(content: str) -> str:
    """Fix struct constructor syntax issues"""
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for struct initialization patterns with issues
        if ('let result = ' in line and '{' in line) or ('let result = ' in lines[i-1:i+1] and '{' in lines[i-1:i+1]):
            # This is likely a struct initialization
            fixed_lines.append(line)
            i += 1
            
            # Collect all lines until we find the closing brace
            struct_lines = []
            brace_count = 0
            in_struct = False
            
            while i < len(lines):
                current_line = lines[i]
                fixed_lines.append(current_line)
                
                brace_count += current_line.count('{') - current_line.count('}')
                
                # Check if this line ends the struct initialization
                if '};' in current_line or '}' in current_line:
                    # Ensure proper formatting
                    if brace_count == 0:
                        # Fix the line to have proper closing
                        if not current_line.strip().endswith('};'):
                            fixed_lines[-1] = current_line.rstrip(',') + '};'
                    break
                
                i += 1
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_double_i_declaration(content: str) -> str:
    """Fix duplicate 'let mut i = 0;' declarations"""
    lines = content.split('\n')
    fixed_lines = []
    i_declaration_found = False
    
    for line in lines:
        if 'let mut i = 0;' in line:
            if not i_declaration_found:
                fixed_lines.append(line)
                i_declaration_found = True
            # Skip duplicate declarations
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_while_loop_structure(content: str) -> str:
    """Fix while loop structures that don't have proper body"""
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for while loops that don't have proper structure
        if 'while i < fields.len()' in line:
            # This while loop likely needs to be removed
            # and replaced with sequential field parsing
            if i + 1 < len(lines) and '// Parse fields with safe defaults' in lines[i + 1]:
                # Skip the while line and add sequential parsing instead
                fixed_lines.append('    // Sequential field parsing')
                # Continue to parse the field assignment lines
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('// Create struct instance'):
                    if 'let ' in lines[j] and '= common_decode::' in lines[j]:
                        # Add this field parsing line with proper increment
                        field_line = lines[j].rstrip(';')
                        fixed_lines.append(f'{field_line};')
                        fixed_lines.append('    i += 1;')
                    j += 1
                
                # Skip until we find the struct creation
                while j < len(lines) and not lines[j].strip().startswith('// Create struct instance'):
                    j += 1
                
                if j < len(lines):
                    fixed_lines.append('')
                    fixed_lines.append(lines[j])  # Add struct creation comment
                
                # Add struct lines
                j += 1
                while j < len(lines) and not lines[j].strip() == '}' and not lines[j].strip() == '    Ok(result)':
                    if lines[j].strip():
                        fixed_lines.append(lines[j])
                    j += 1
                
                if j < len(lines) and (lines[j].strip() == '}' or lines[j].strip() == '    Ok(result)'):
                    fixed_lines.append(lines[j])
                
                # Skip the remaining lines of the while loop
                while j < len(lines) and not lines[j].strip().startswith('Ok(result)'):
                    j += 1
                
                i = j
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_parser_file(file_path: Path) -> bool:
    """Fix a single parser file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_double_i_declaration(content)
        content = fix_while_loop_structure(content)
        content = fix_struct_constructor_syntax(content)
        
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
    """Fix all generated parser files with delimiter issues"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found!")
        return
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        # Check if file has the problematic patterns
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if ('let mut i = 0;' in content and content.count('let mut i = 0;') > 1) or \
               ('while i < fields.len()' in content and '    }' not in content[content.find('while i < fields.len()'):]) or \
               ('    };' not in content and 'let result =' in content):
                
                if fix_parser_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with delimiter issues")

if __name__ == "__main__":
    main()