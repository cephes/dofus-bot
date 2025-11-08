import os
from pathlib import Path

# Fix JSON field names in action files by adding quotes
actions_dir = Path("core/src/retroproto_parsers/generated/actions")

fixed_files = 0

for rs_file in actions_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the specific patterns in json! macros
        content = content.replace('    serde_json::json!({', '    serde_json::json!({')
        
        # Fix unquoted field names in json! macros
        import re
        # Pattern: field_name: m.field_name -> "field_name": m.field_name
        def fix_json_field(match):
            field_name = match.group(1)
            value = match.group(2)
            return f'"{field_name}": {value}'
        
        # Look for patterns like: field_name: m.field_name,
        pattern = r'([a-zA-Z_][a-zA-Z0-9_]*):\s*m\.([a-zA-Z_][a-zA-Z0-9_]*)'
        content = re.sub(pattern, fix_json_field, content)
        
        if content != original_content:
            with open(rs_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rs_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rs_file}: {e}")

print(f"Fixed {fixed_files} action files")