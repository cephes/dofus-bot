import os
import re
from pathlib import Path

# Create a specific fix for the exact pattern we're seeing
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern: Ok(StructName {}) // comment
        # This is the exact pattern we keep seeing
        content = re.sub(
            r'(\s+)Ok\(([^)]+)\)\s+\n(\s+)// Some variants ignore payload in Go; we still succeed but you can switch to strict:\n(\s+)// return Err\([^)]+\);\s*\n(\s+)\}',
            r'\1// Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3// return Err(format!("expected empty payload for \2, got: {{}}", p));\n\1Ok(\2 {})\n\5',
            content,
            flags=re.MULTILINE
        )
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")