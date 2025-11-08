#!/usr/bin/env python3

import os
import re

def fix_remaining_syntax_errors():
    """Fix remaining syntax errors with more aggressive patterns"""
    
    generated_dir = "core/src/retroproto_parsers/generated"
    count = 0
    
    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            if file.endswith('.rs'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Fix: Pattern where we have Ok(StructName { field: value }}) - remove the extra }
                    content = re.sub(r'Ok\(([^}]+)\}\}\)$', r'Ok(\1})', content)
                    
                    # Fix: Remove any trailing braces immediately before closing parentheses
                    content = re.sub(r'\}\s*\)\s*$', '})', content)
                    
                    # Fix: Remove any extra closing braces
                    content = re.sub(r'}}\s*$', '})', content)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        print(f"Fixed: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\nFixed remaining syntax errors in {count} files")

if __name__ == "__main__":
    fix_remaining_syntax_errors()