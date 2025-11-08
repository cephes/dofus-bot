import os
import re
from pathlib import Path

# Fix all files that were corrupted by the global_fix.py script
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix files that have {struct_name} literal strings (from the broken global_fix.py)
        if '{struct_name}' in content:
            # Get the actual struct name from the file
            struct_match = re.search(r'pub struct (\w+) \{\}', content)
            if struct_match:
                struct_name = struct_match.group(1)
                
                # Replace {struct_name} with the actual struct name
                content = content.replace('{struct_name}', struct_name)
        
        # Remove any duplicate lines that might have been created
        lines = content.split('\n')
        seen = set()
        clean_lines = []
        for line in lines:
            if line.strip() and line not in seen:
                clean_lines.append(line)
                seen.add(line)
        
        content = '\n'.join(clean_lines)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")