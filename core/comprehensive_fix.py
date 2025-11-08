#!/usr/bin/env python3

import os
import re

def fix_comprehensive_syntax_errors(content):
    """Apply all known syntax fixes to the content"""
    
    lines = content.split('\n')
    fixed_lines = []
    changes = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix 1: Missing closing brace and parenthesis in Ok() expressions
        # Pattern: Ok(Struct { ... field: value; -> Ok(Struct { ... field: value });
        if ('Ok(' in line and 
            '{' in line and 
            line.rstrip().endswith(';') and 
            not line.rstrip().endswith('});') and
            ('parts.get' in line or 'unwrap_or_default' in line or 'and_then' in line or 'map(' in line)):
            
            # Remove trailing ; and add })
            line = line.rstrip(';') + '})'
            changes += 1
        
        # Fix 2: Lines ending with ; where Ok expression needs closing
        elif ('Ok(' in line and 
              line.rstrip().endswith(';') and 
              not line.rstrip().endswith('});') and
              not line.rstrip().endswith(');')):
            
            # This is likely an incomplete Ok expression
            line = line.rstrip(';') + '})'
            changes += 1
        
        # Fix 3: Fix double semicolons
        if ';;' in line:
            line = line.replace(';;', ';')
            changes += 1
        
        # Fix 4: Fix pattern like ); }; -> };
        if line.strip() == '); }':
            line = '});'
            changes += 1
        
        # Fix 5: Fix extra closing parentheses
        if ' );' in line:
            line = line.replace(' );', ';')
            changes += 1
        
        # Fix 6: Fix pattern: Ok(Struct { ... }); -> Ok(Struct { ... });
        # Ensure Ok expressions are properly closed
        if 'Ok(' in line and line.rstrip().endswith(')') and not line.rstrip().endswith('});'):
            # Add closing brace
            line = line.rstrip(')') + '})'
            changes += 1
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines), changes

def process_file(file_path):
    """Process a single file and return number of changes made"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, changes = fix_comprehensive_syntax_errors(content)
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
        
        return changes
        
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        return 0

def main():
    base_dir = 'src'
    total_changes = 0
    changed_files = 0
    
    print('Applying comprehensive syntax fixes...')
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                changes = process_file(file_path)
                if changes > 0:
                    total_changes += changes
                    changed_files += 1
                    print(f'Fixed {changes} issues in {file_path}')
    
    print(f'Fixed {total_changes} issues in {changed_files} files')

if __name__ == "__main__":
    main()