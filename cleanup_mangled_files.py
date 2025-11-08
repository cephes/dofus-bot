#!/usr/bin/env python3
"""
Clean up files with placeholder text and fix them properly.
"""
import os
import re
import glob

def fix_mangled_file(filepath):
    """Fix files that have been mangled with placeholder text."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Skip if file doesn't have placeholder text
        if 'TO_JSON_FUNCTION_PLACEHOLDER' not in content and 'STRUCT_NAME_PLACEHOLDER' not in content:
            return False
        
        # Extract the actual struct and function name from the file
        struct_match = re.search(r'pub struct (\w+)', content)
        func_match = re.search(r'pub fn parse_(\w+)\(', content)
        
        if not struct_match or not func_match:
            print(f"  -> Could not extract names from {filepath}")
            return False
            
        struct_name = struct_match.group(1)
        func_name = func_match.group(1)
        
        # Clean up the content - remove duplicate/broken sections
        # First, let's find the main structure
        lines = content.split('\n')
        cleaned_lines = []
        
        # Keep everything until the first broken section
        skip_until_end = False
        for i, line in enumerate(lines):
            # Skip lines with placeholders
            if 'TO_JSON_FUNCTION_PLACEHOLDER' in line or 'STRUCT_NAME_PLACEHOLDER' in line:
                skip_until_end = True
                continue
            
            # Skip orphaned braces and else blocks
            if line.strip() in ['} else {', '}', '} else {', '    }', '    } else {']:
                continue
                
            # Skip duplicate function endings
            if line.strip() == '}' and i > 0 and lines[i-1].strip() == '}':
                continue
                
            if not skip_until_end:
                cleaned_lines.append(line)
                
            # Reset skip flag when we hit a proper new function
            if 'pub fn ' in line and 'TO_JSON_FUNCTION_PLACEHOLDER' not in line:
                skip_until_end = False
        
        # Now reconstruct the file properly
        clean_content = '\n'.join(cleaned_lines)
        
        # Ensure the file ends properly
        if not clean_content.strip().endswith('}'):
            clean_content += '\n}\n'
            
        # Write the cleaned content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_content)
            
        print(f"  -> Cleaned up {filepath}")
        return True
        
    except Exception as e:
        print(f"  -> Error cleaning {filepath}: {e}")
        return False

def main():
    parser_files = glob.glob("core/src/retroproto_parsers/generated/*.rs")
    parser_files.extend(glob.glob("core/src/retroproto_parsers/generated/actions/*.rs"))
    
    fixed_count = 0
    total_count = len(parser_files)
    
    print(f"Checking {total_count} parser files for mangled content...")
    
    for filepath in parser_files:
        if fix_mangled_file(filepath):
            fixed_count += 1
    
    print(f"Cleaned up {fixed_count} mangled parser files")

if __name__ == "__main__":
    main()