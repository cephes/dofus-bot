import os
from pathlib import Path

# Fix JSON field names in action files
actions_dir = Path("core/src/retroproto_parsers/generated/actions")

fixed_files = 0

for rs_file in actions_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the JSON field names to be quoted
        # Pattern: field_name: m.field_name -> "field_name": m.field_name
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            if 'serde_json::json!({' in line or any(':' in l and 'm.' in l for l in fixed_lines[-5:]):
                # This is inside a json! macro, fix the field names
                if ':' in line and 'm.' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        field_name = parts[0].strip()
                        value_part = ':'.join(parts[1:]).strip()
                        # Quote the field name
                        line = f'"{field_name}": {value_part}'
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