import os
import re
from pathlib import Path

# Fix the specific pattern: } else { // comment only } 
# by adding Ok(StructName {}) before the final }

generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Find lines with else { followed by only comments then }
        lines = content.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            
            # Check if this is an else line
            if 'else {' in line and i + 1 < len(lines):
                # Look ahead to see if else block only has comments
                j = i + 1
                has_code = False
                struct_name = None
                
                # Find the struct name from previous Ok() call
                for k in range(i - 1, max(0, i - 10), -1):
                    if 'Ok(' in lines[k]:
                        match = re.search(r'Ok\(([^ {\n]+)', lines[k])
                        if match:
                            struct_name = match.group(1).strip()
                            break
                
                # Check what's in the else block
                while j < len(lines) and lines[j].strip() != '}':
                    if lines[j].strip() and not lines[j].strip().startswith('//'):
                        has_code = True
                        break
                    j += 1
                
                # If no code and we found struct name, add return
                if not has_code and struct_name and j < len(lines):
                    # Insert the return statement before the closing brace
                    new_lines.append(f'        Ok({struct_name} {{}})')
            
            i += 1
        
        new_content = '\n'.join(new_lines)
        
        if new_content != original:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")