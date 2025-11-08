#!/usr/bin/env python3
"""
Fix systematic issues in generated Rust parser files

This script fixes:
- Missing loop variable 'i' in parser functions
- Missing field iteration loops
- Generic type parameter issues
- Missing field parsing logic
"""

import os
import re
from pathlib import Path

def fix_parser_function(file_path: Path) -> bool:
    """Fix a single parser file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        lines = content.split('\n')
        
        # Check if this file has the typical pattern of missing 'i' variable
        has_missing_i = any("fields.get(i)" in line and "let i = " not in content for line in lines)
        
        if not has_missing_i:
            return False
        
        # Look for the pattern where we need to add a loop
        # Find the line with let fields = ... and add the missing loop
        new_lines = []
        added_loop = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # After split_fields line, add the missing loop
            if 'let fields = common_decode::split_fields(payload);' in line and not added_loop:
                # Add loop variable declaration
                new_lines.append('    let mut i = 0;')
                new_lines.append('    ')
                # Add the loop structure
                new_lines.append('    // Parse each field')
                new_lines.append('    while i < fields.len() {')
                added_loop = True
                
                # Now we need to find the field parsing lines and fix them
                # and close the loop at the end
                
                # Look ahead to find where to close the loop
                # We'll handle this in a second pass
        
        if not added_loop:
            return False
            
        # Second pass: find the end of function and close the loop there
        final_lines = []
        brace_count = 0
        in_function = False
        loop_started = False
        
        for line in final_lines:
            if not in_function:
                final_lines.append(line)
                if 'pub fn parse_' in line:
                    in_function = True
                continue
                    
            final_lines.append(line)
            
            # Count braces to find end of function
            brace_count += line.count('{') - line.count('}')
            
            # If we hit the end of the function, close the loop
            if brace_count == 0 and in_function:
                if loop_started:
                    final_lines.append('    }')
                break
                
            if 'while i < fields.len()' in line:
                loop_started = True
        
        # If we couldn't parse the structure properly, let's do a simpler fix
        if not final_lines or len(final_lines) < len(new_lines):
            # Use the new_lines approach
            content = '\n'.join(new_lines)
        else:
            content = '\n'.join(final_lines)
        
        # Additional fixes for specific patterns
        
        # Fix the 'typ' generic parameter issue
        content = re.sub(r'pub items: Vec<typ>,', r'pub items: Vec<String>,', content)
        content = re.sub(r'pub struct \w+<typ>', r'pub struct \g<0> {', content)
        
        # If we still have missing 'i' variables, let's try a more direct approach
        if 'fields.get(i)' in content and 'let i = ' not in content:
            # Split by lines and add i = 0 at the beginning
            lines = content.split('\n')
            new_lines = []
            i_added = False
            
            for line in lines:
                if 'let fields = common_decode::split_fields(payload);' in line:
                    new_lines.append(line)
                    new_lines.append('    let mut i = 0;')
                    i_added = True
                else:
                    new_lines.append(line)
            
            if i_added:
                content = '\n'.join(new_lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
            
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_specific_issues():
    """Fix specific known issues in generated files"""
    
    # Fix the AccountCharacterSelectedSuccess struct
    account_char_file = Path("core/src/retroproto_parsers/generated/AccountCharacterSelectedSuccess.rs")
    if account_char_file.exists():
        with open(account_char_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the generic parameter issue
        content = content.replace('pub struct AccountCharacterSelectedSuccess<typ> {', 'pub struct AccountCharacterSelectedSuccess {')
        content = content.replace('pub items: Vec<typ>,', 'pub items: Vec<String>,')
        
        with open(account_char_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed generic type issue: {account_char_file}")

def main():
    """Fix all generated parser files with systematic issues"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found!")
        return
    
    # First fix specific known issues
    fix_specific_issues()
    
    # Then fix all parser files
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
            
        if fix_parser_function(rs_file):
            fixed_files += 1
    
    print(f"\nFixed {fixed_files} files with systematic parser issues")

if __name__ == "__main__":
    main()