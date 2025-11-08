import os
import re
from pathlib import Path

# Comprehensive fix for all files with the problematic pattern
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

def fix_file(file_path):
    """Fix the specific pattern in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # The exact pattern we're seeing repeatedly:
        # Ok(StructName {}) // comment
        # This should become:
        # // comment
        # Ok(StructName {})
        
        # First, let's find all instances
        pattern = r'Ok\(([^)]+)\)\s+// Some variants ignore payload in Go; we still succeed but you can switch to strict:'
        matches = list(re.finditer(pattern, content))
        
        if matches:
            # Get struct name from the file
            struct_match = re.search(r'pub struct (\w+) \{\}', content)
            if struct_match:
                struct_name = struct_match.group(1)
                
                # Replace the pattern
                content = re.sub(pattern, f'// Some variants ignore payload in Go; we still succeed but you can switch to strict:', content)
                
                # Add the Ok call before the closing brace
                content = re.sub(r'(\s+)\}', r'\1    Ok({struct_name} {})\n\1}', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Process all files
for rust_file in generated_dir.rglob("*.rs"):
    if fix_file(rust_file):
        print(f"Fixed: {rust_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")