import os
import re
from pathlib import Path

# Fix remaining syntax issues - specifically the extra closing braces
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
        content = re.sub(r'\}\}\s*$', '', content)  # Remove '}}' at end of lines
        content = re.sub(r'\}\}\s*\)', '})', content)  # Fix '}}' followed by ')'
        
        # Fix malformed struct definitions
        content = re.sub(r'pub\s+struct\s+\w+\s*\{\s*pub\s+', 'pub struct \\1 {\n  pub ', content)
        
        # Fix function definitions that are missing proper structure
        if 'pub fn parse_' in content and 'if p.is_empty()' in content:
            # This is a malformed function, try to fix it
            if 'let p = payload.trim_end_matches' not in content:
                content = content.replace(
                    'let parts: Vec<&str> = if p.is_empty() { vec![] }',
                    'let p = payload.trim_end_matches(\'\\0\');\n  let parts: Vec<&str> = if p.is_empty() { vec![] }'
                )
        
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