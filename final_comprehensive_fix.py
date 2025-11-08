import os
import re
from pathlib import Path

# Final comprehensive fix for all remaining syntax errors
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix missing closing braces for functions
        lines = content.split('\n')
        fixed_lines = []
        in_function = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Add the line
            fixed_lines.append(line)
            
            # Check if this is a function definition
            if stripped.startswith('pub fn ') and '(' in stripped and ')' in stripped:
                in_function = True
            
            # Check if we need to add closing brace
            if in_function and stripped.startswith('pub fn ') and not stripped.endswith('{'):
                # This is a new function without opening brace, add closing brace for previous function
                if i > 0 and not any(lines[j].strip().endswith('}') for j in range(len(fixed_lines)-1, max(-1, len(fixed_lines)-10), -1)):
                    fixed_lines.append('}')
                in_function = True
            
            # Mark function end
            if in_function and stripped.endswith('}') and 'pub fn ' not in stripped:
                in_function = False
        
        content = '\n'.join(fixed_lines)
        
        # Final cleanup - ensure each function has proper closing
        content = re.sub(r'pub fn \w+.*?\([^)]*\) -> .*? \{[^}]*\}(?!\s*\}\s*pub fn)', lambda m: m.group(0) + '\n}', content)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")