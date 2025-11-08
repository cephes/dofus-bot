import os
import re
from pathlib import Path

# Comprehensive cleanup of all generated files
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove duplicate lines
        lines = content.split('\n')
        seen = set()
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and line not in seen:
                clean_lines.append(line)
                seen.add(line)
        
        content = '\n'.join(clean_lines)
        
        # Fix duplicate Ok() calls on consecutive lines
        content = re.sub(r'Ok\([^)]+\)\s*\n\s*Ok\([^)]+\)', '', content)
        
        # Remove any extra closing braces/parentheses at end of file
        content = re.sub(r'\}\s*\}\s*$', '}', content)
        content = re.sub(r'\)\s*\)\s*$', ')', content)
        
        # Ensure each function ends with proper closing
        content = re.sub(r'pub fn \w+.*?\([^)]*\) -> .*? \{[^}]*\}(?![\r\n]*\})', 
                        lambda m: m.group(0) + '}', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")