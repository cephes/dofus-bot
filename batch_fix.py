import os
import re
from pathlib import Path

# Find all generated Rust files and fix the specific pattern
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

# Pattern to match: Ok() before comment in else block
pattern = r'(\s+)else \{\s*\n\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n\3// return Err\([^)]+\);\s*\}'

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply the fix
        new_content = re.sub(pattern, r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}', content, flags=re.MULTILINE | re.DOTALL)
        
        if new_content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")