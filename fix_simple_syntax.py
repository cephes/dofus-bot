import os
from pathlib import Path

# Simple fix for remaining syntax issues
generated_dir = Path("core/src/retroproto_parsers/generated")

# Count all .rs files to verify we have all 450
total_files = 0
fixed_files = 0

for rust_file in generated_dir.rglob("*.rs"):
    total_files += 1
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the specific issue: remove line 15 which has an extra '}'
        lines = content.split('\n')
        
        # Check if last line is just a '}' and remove it
        if len(lines) > 0 and lines[-1].strip() == '}':
            lines = lines[:-1]  # Remove the last line
            content = '\n'.join(lines)
        
        # Fix any remaining extra '}}' in code
        content = content.replace('}}', '}')
        
        # Fix malformed struct definitions by adding proper braces
        if 'pub struct' in content and '{' not in content and '}' in content:
            content = content.replace('pub struct', 'pub struct ')
        
        # Remove any trailing empty lines
        content = content.rstrip()
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_files} out of {total_files} files")

# Also check for files that might need proper Rust syntax
problematic_patterns = [
    ('} else {', '    } else {'),
    ('Ok(', '  Ok('),
    ('pub fn ', 'pub fn '),
    ('#[derive', '#[derive'),
    ('use serde', 'use serde'),
]

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = content
        for pattern, replacement in problematic_patterns:
            if pattern in content and pattern != replacement:
                fixed_content = fixed_content.replace(pattern, replacement)
        
        if fixed_content != content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Pattern-fixed: {rust_file}")
            
    except Exception as e:
        print(f"Error in pattern fix for {rust_file}: {e}")