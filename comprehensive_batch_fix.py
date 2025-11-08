import os
import re
from pathlib import Path

# More comprehensive fix for all files with the pattern
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Multiple patterns to fix
        # Pattern 1: Ok() before comment in else block
        content = re.sub(
            r'(\s+)else \{\s*\n\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n\3// return Err\([^)]+\);\s*\}',
            r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Pattern 2: Ok() before comment in else block (simpler)
        content = re.sub(
            r'(\s+)else \{\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n\3// return Err\([^)]+\);\s*\}\s*',
            r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}',
            content,
            flags=re.MULTILINE
        )
        
        # Pattern 3: Fix missing imports
        if 'use serde_json::' not in content and 'json!' in content:
            content = re.sub(
                r'use serde::\{Serialize, Deserialize\};',
                'use serde::{Serialize, Deserialize};\nuse serde_json::{Value, json};',
                content
            )
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")