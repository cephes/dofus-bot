#!/usr/bin/env python3

import os
import re

def fix_all_delimiter_issues():
    """Fix all delimiter issues with comprehensive patterns"""
    
    generated_dir = "core/src/retroproto_parsers/generated"
    count = 0
    
    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            if file.endswith('.rs'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    original_lines = lines.copy()
                    
                    for i, line in enumerate(lines):
                        # Fix Ok(StructName { ... }}) pattern - remove extra }
                        if 'Ok(' in line and '})}' in line:
                            lines[i] = line.replace('})}', '})')
                        
                        # Fix Ok(StructName { ... }} pattern - remove extra }
                        if 'Ok(' in line and '}}' in line and line.strip().endswith('}}'):
                            lines[i] = line.rstrip()[:-1] + '\n'
                        
                        # Remove any line that ends with more than one closing brace
                        if re.match(r'.*\}\}\)+$', line.strip()):
                            line_clean = re.sub(r'\}\}\)+$', '}', line.strip())
                            if line_clean != line.strip():
                                lines[i] = line_clean + '\n'
                    
                    if lines != original_lines:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                        count += 1
                        print(f"Fixed: {filepath}")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\nFixed delimiter issues in {count} files")

if __name__ == "__main__":
    fix_all_delimiter_issues()