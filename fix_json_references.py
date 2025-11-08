import os
from pathlib import Path

# Fix JSON field references in action files
actions_dir = Path("core/src/retroproto_parsers/generated/actions")

fixed_files = 0

for rs_file in actions_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the JSON field references
        # Pattern: "field_name": field_name -> "field_name": m.field_name
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            if 'serde_json::json!({' in line:
                # Found the start of json macro
                fixed_lines.append(line)
                continue
            elif line.strip().endswith('})'):
                # End of json macro
                fixed_lines.append(line)
                continue
            elif ':' in line and line.strip().startswith('"') and line.strip().endswith(','):
                # This is a field line in the json macro
                parts = line.split(':', 1)
                field_name = parts[0].strip().strip('"')
                value_part = parts[1].strip().rstrip(',')
                
                # Extract the value without m. prefix and add it back
                if value_part in ['dir_and_cells', 'sprite_id', 'cinematic', 'challenger_id', 'challenged_id', 'error_reason']:
                    line = f'        "{field_name}": m.{value_part},'
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        if content != original_content:
            with open(rs_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rs_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rs_file}: {e}")

print(f"Fixed {fixed_files} action files")