import os
import re
from pathlib import Path

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # Fix the }} pattern
    content = content.replace('}})', '})')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    if fix_file(rust_file):
        print(f"Fixed: {rust_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")