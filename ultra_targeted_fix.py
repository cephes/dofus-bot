import os
import re
from pathlib import Path

# Create a very specific fix for the exact pattern we're seeing
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # The exact pattern we're seeing: Ok() before comment in else block
        # This is the specific pattern that needs to be fixed
        pattern = r'(\s+)else \{\s*\n\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants ignore payload in Go; we still succeed but you can switch to strict:\n(\s+)// return Err\(format!\("expected empty payload for [^"]+", got: \{\}", p\)\);\s*\}\s*'
        
        def replace_func(match):
            indent1 = match.group(1)
            struct_name = match.group(2)
            indent2 = match.group(3)
            indent3 = match.group(4)
            
            return f'{indent1}else {{\n{indent2}    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n{indent2}    // return Err(format!("expected empty payload for {struct_name}, got: {{}}", p));\n{indent2}    Ok({struct_name} {{}})\n{indent1}}}'
        
        content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")