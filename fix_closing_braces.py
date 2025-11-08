import os
from pathlib import Path

# Fix extra closing braces in all generated files
generated_dir = Path("core/src/retroproto_parsers/generated")

fixed_files = 0

for rs_file in generated_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the extra closing brace at the end of Ok() statements
        content = content.replace('}})', '})')
        
        # Remove any extra closing braces at the end of functions
        content = content.replace('}})', '})')
        
        if content != original_content:
            with open(rs_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rs_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rs_file}: {e}")

print(f"Fixed {fixed_files} files")