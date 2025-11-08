#!/usr/bin/env python3

import os
import re

def fix_missing_closing_braces(file_path):
    """Fix missing closing braces in Ok() expressions"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            
            # Fix pattern: Ok(Struct { ... }) );
            # Should be: Ok(Struct { ... });
            if 'Ok(' in line and line.rstrip().endswith(')'):
                # Check if it's missing the closing brace for the struct
                if line.count('Ok(') > 0 and '{' in line and '})' in line:
                    # Pattern: Ok(Struct { ... })  - missing }
                    line = line.replace('})', '})').replace(') )', ')')
                elif line.count('Ok(') > 0 and '{' in line and line.count('}') == 0:
                    # Pattern: Ok(Struct { ... )  - missing }
                    line = line.rstrip(')') + '})'
                    changes += 1
            # Fix pattern: Ok(Struct { ... }  - missing )
            elif 'Ok(' in line and line.rstrip().endswith('}') and not line.rstrip().endswith('})'):
                line = line.rstrip() + '}'
                changes += 1
            
            fixed_lines.append(line)
        
        if changes > 0:
            content = '\n'.join(fixed_lines)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    base_dir = "src"
    total_files = 0
    total_changes = 0
    
    print("Fixing missing closing braces...")
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                changes = fix_missing_closing_braces(file_path)
                if changes > 0:
                    total_changes += changes
                    print(f"Fixed {changes} issues in {file_path}")
                total_files += 1
    
    print(f"Found {total_files} .rs files")
    print(f"Total changes applied: {total_changes}")

if __name__ == "__main__":
    main()