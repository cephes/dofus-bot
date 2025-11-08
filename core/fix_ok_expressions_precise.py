#!/usr/bin/env python3

import os
import re

def fix_ok_expressions_precise(file_path):
    """Fix missing semicolons in Ok() expressions - more precise version"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix pattern: Ok(...) followed by } without semicolon
        # Look for: Ok(AccountCommunity { ... }) }
        # Replace with: Ok(AccountCommunity { ... });
        
        # Use a more precise regex that checks for the pattern
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            
            # Only fix if it looks like: Ok(...) followed directly by }
            # and doesn't already end with );
            if ('Ok(' in line and 
                line.strip().endswith('}') and 
                not line.rstrip().endswith(');') and
                not line.rstrip().endswith(') }')):
                
                # Remove trailing } and add );
                line = line.rstrip() + ';'
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
    
    print("Scanning for .rs files with precision...")
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                changes = fix_ok_expressions_precise(file_path)
                if changes > 0:
                    total_changes += changes
                    print(f"Fixed {changes} issues in {file_path}")
                total_files += 1
    
    print(f"Found {total_files} .rs files")
    print(f"Total changes applied: {total_changes}")

if __name__ == "__main__":
    main()