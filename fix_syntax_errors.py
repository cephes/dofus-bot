import os
import re
from pathlib import Path

# Fix the remaining syntax errors
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix import syntax
        content = content.replace('use serde{Serialize, Deserialize};', 'use serde::{Serialize, Deserialize};')
        
        # Fix extra closing braces in conditional expressions
        content = re.sub(r'if\s+[^}]+\{\s*vec!\[\]\s*\}\}\s*else\s*\{', 
                        lambda m: m.group(0).replace('}}', '}'), content)
        
        # Fix extra closing braces/parentheses in Ok() calls
        content = re.sub(r'Ok\([^)]+\}\}\)', lambda m: m.group(0).replace('}})', ')'), content)
        content = re.sub(r'Ok\([^)]+\}\s*\}\s*\)', lambda m: m.group(0).replace('})', ')'), content)
        
        # Fix duplicate lines and missing function separators
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            if line.strip() and line not in clean_lines:
                clean_lines.append(line)
        
        # Ensure proper function separation
        content = '\n'.join(clean_lines)
        
        # Fix missing closing braces for functions
        content = re.sub(r'pub fn \w+.*?\([^)]*\) -> .*? \{[^}]*\}\s*pub fn', 
                        lambda m: m.group(0) + '\n}', content)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")