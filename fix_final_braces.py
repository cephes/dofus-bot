import os
from pathlib import Path

# Fix the remaining extra closing braces issue
generated_dir = Path("core/src/retroproto_parsers/generated")

fixed_files = 0

for rs_file in generated_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the specific pattern: Ok(...) }) followed by } on the next line
        if '}) }' in content:
            # Find lines that end with '}) }' and fix them
            lines = content.split('\n')
            fixed_lines = []
            for line in lines:
                if line.strip().endswith('}) }'):
                    # This line has the extra closing brace
                    line = line.replace('}) }', '})')
                fixed_lines.append(line)
            content = '\n'.join(fixed_lines)
        
        if content != original_content:
            with open(rs_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rs_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rs_file}: {e}")

print(f"Fixed {fixed_files} files")