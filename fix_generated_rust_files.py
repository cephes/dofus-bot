#!/usr/bin/env python3

import os
import re

def fix_generated_rust_files():
    """Fix all generated Rust files with proper syntax"""
    
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
                    
                    # Fix 1: Remove duplicate Ok() lines  
                    lines = content.split('\n')
                    fixed_lines = []
                    seen_ok_lines = set()
                    
                    for line in lines:
                        # Skip duplicate Ok lines
                        if line.strip().startswith('Ok(') and line.strip() in seen_ok_lines:
                            continue
                        if line.strip().startswith('Ok('):
                            seen_ok_lines.add(line.strip())
                        fixed_lines.append(line)
                    
                    content = '\n'.join(fixed_lines)
                    
                    # Fix 2: Remove extra closing braces and parentheses
                    content = re.sub(r'}\)\s*}\s*\)\s*$', '})', content)
                    content = re.sub(r'}\s*}\s*\)\s*$', '})', content)
                    content = re.sub(r'\)\s*}\s*$', '})', content)
                    
                    # Fix 3: Fix the function closing
                    content = re.sub(r'}\s*}\s*$', '}', content)
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        print(f"Fixed: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\nFixed syntax in {count} files")

if __name__ == "__main__":
    fix_generated_rust_files()