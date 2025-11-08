import os
import re
from pathlib import Path

# Final comprehensive fix for all remaining syntax errors
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix import syntax issues
        content = content.replace('use serde{Serialize, Deserialize};', 'use serde::{Serialize, Deserialize};')
        content = content.replace('use serde_json{Value, json};', 'use serde_json::{Value, json};')
        
        # Fix extra closing braces and parentheses
        content = re.sub(r'\}\}\)', '})', content)
        content = re.sub(r'Ok\([^)]+\}\}\)', lambda m: m.group(0).replace('}})', ')'), content)
        
        # Fix any remaining malformed syntax
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            # Keep the line but fix common issues
            line = line.strip()
            if line:
                # Remove duplicate empty functions
                if 'pub fn ' in line and '()' in line and not line.endswith('{') and not line.endswith(';'):
                    # This might be a malformed function
                    continue
                if line.startswith('//') or line.startswith('use ') or line.startswith('pub ') or line.startswith('#[derive') or '{' in line or '}' in line or 'Ok(' in line:
                    clean_lines.append(line)
        
        content = '\n'.join(clean_lines)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")