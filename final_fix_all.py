import os
import re
from pathlib import Path

# Final comprehensive fix for ALL remaining files
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Ok() before comment (the most common one)
        content = re.sub(
            r'(\s+)else \{\s*\n\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n\3// return Err\([^)]+\);\s*\}',
            r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Pattern 2: Simpler version
        content = re.sub(
            r'(\s+)else \{\s*Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n\3// return Err\([^)]+\);\s*\}',
            r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}',
            content,
            flags=re.MULTILINE
        )
        
        # Pattern 3: Ok() with comment on same line
        content = re.sub(
            r'(\s+)else \{\s*Ok\(([^)]+)\)\s*// Some variants.*?\n(\s+)// return Err\([^)]+\);\s*\}',
            r'\1else {\n\3    // Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3    // return Err(format!("expected empty payload for \2, got: {}", p));\n\3    Ok(\2 {})\n\1}',
            content,
            flags=re.MULTILINE
        )
        
        # Pattern 4: If there are any remaining stray Ok() before comment
        content = re.sub(
            r'(\s+)Ok\(([^)]+)\)\s*\n(\s+)// Some variants.*?\n(\s+)\}',
            r'\1// Some variants ignore payload in Go; we still succeed but you can switch to strict:\n\3// return Err(format!("expected empty payload for \2, got: {}", p));\n\1Ok(\2 {})\n\4',
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