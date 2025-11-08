#!/usr/bin/env python3

import os
import re

def fix_final_syntax_errors():
    """Fix final syntax errors in generated Rust files"""
    
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
                    
                    # Fix 1: Replace }} }) at end of Ok(...) calls
                    content = re.sub(r'\) }\}$\)', ') }', content)
                    content = re.sub(r'\) }\}\)$', ')', content)
                    
                    # Fix 2: Replace extra closing braces in Ok() calls
                    content = re.sub(r'Ok\(\{([^}]*)\}\}\)$', r'Ok({\1})', content)
                    
                    # Fix 3: Fix specific pattern with Ok(Struct { field }})
                    content = re.sub(r'Ok\(([^}]+)\}\}\)$', r'Ok(\1})', content)
                    
                    # Fix 4: Remove trailing braces
                    content = re.sub(r'\}\s*\)\s*$', '})', content)
                    
                    # Fix 5: Remove any remaining trailing whitespace and extra braces
                    content = content.rstrip()
                    content = re.sub(r'\}\s*$', '}', content)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        print(f"Fixed: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\nFixed syntax errors in {count} files")

if __name__ == "__main__":
    fix_final_syntax_errors()