import os
from pathlib import Path

# Targeted fix for if-else syntax and missing parts
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
        
        # Fix the broken if-else syntax
        # Pattern 1: if condition { vec![] } else { collect() };
        content = content.replace(
            'let parts: Vec<&str> = if p.is_empty() { vec![] }',
            'let parts: Vec<&str> = if p.is_empty() { vec![] }'
        )
        
        # Fix the if-else continuation
        if '} else { p.split' in content:
            # Find the exact broken pattern and fix it
            lines = content.split('\n')
            fixed_lines = []
            for i, line in enumerate(lines):
                if 'let parts: Vec<&str> = if p.is_empty() { vec![] }' in line and i + 1 < len(lines):
                    # This line and the next need to be combined properly
                    next_line = lines[i + 1]
                    if '} else { p.split' in next_line:
                        # Combine them properly
                        fixed_lines.append(line + ' else { p.split(\'|\').collect() };')
                        i += 1  # Skip the next line since we combined it
                    else:
                        fixed_lines.append(line)
                elif '} else { p.split' in line:
                    # This line should be skipped as it was combined above
                    continue
                else:
                    fixed_lines.append(line)
            content = '\n'.join(fixed_lines)
        
        # Add missing variable declaration at the beginning of parse functions
        if 'pub fn parse_' in content and 'let p = ' not in content:
            # Find the function definition and add the variable declaration
            lines = content.split('\n')
            fixed_lines = []
            for i, line in enumerate(lines):
                fixed_lines.append(line)
                if 'pub fn parse_' in line and i + 1 < len(lines):
                    # Add the variable declaration on the next line
                    fixed_lines.append('  let p = payload.trim_end_matches(\'\\0\');')
            content = '\n'.join(fixed_lines)
        
        # Fix missing semicolons after Ok() returns
        if content.count('Ok(') > 0 and not content.strip().endswith(';'):
            # Add semicolon to the last line if it's a return statement
            lines = content.split('\n')
            if lines and 'Ok(' in lines[-1]:
                lines[-1] = lines[-1] + ';'
            content = '\n'.join(lines)
        
        # Fix missing closing braces for function
        if 'pub fn parse_' in content and not content.rstrip().endswith('}'):
            content = content.rstrip() + '\n}'
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_files} out of {total_files} files")