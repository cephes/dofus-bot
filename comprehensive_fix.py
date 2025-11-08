import os
from pathlib import Path
import re

# Comprehensive fix for all remaining issues
generated_dir = Path("core/src/retroproto_parsers/generated")
actions_dir = Path("core/src/retroproto_parsers/generated/actions")

fixed_files = 0

for rs_file in generated_dir.rglob("*.rs"):
    try:
        with open(rs_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove duplicate Ok() statements
        lines = content.split('\n')
        if len(lines) > 2:
            # Look for duplicate Ok statements on consecutive lines
            i = 0
            while i < len(lines) - 1:
                if lines[i].strip().startswith('Ok(') and lines[i+1].strip().startswith('Ok('):
                    # Remove the first Ok statement
                    lines[i] = ''
                    # Make sure the second one has a semicolon
                    if not lines[i+1].strip().endswith('}'):
                        lines[i+1] = lines[i+1].rstrip() + ' }'
                i += 1
            content = '\n'.join(lines)
        
        # Fix 2: Add missing semicolons
        content = re.sub(r'Ok\([^)]+\)\s*\n\s*Ok\(', 'Ok(', content)
        content = re.sub(r'Ok\([^)]+\)\s*$', lambda m: m.group(0) + ';', content)
        
        # Fix 3: Rename 'type' field to 'type_'
        content = content.replace('pub type: i64,', 'pub type_: i64,')
        content = content.replace('type:', 'type_:')
        
        # Fix 4: Fix function name inconsistencies
        content = content.replace('parse_AccountAddCharacter', 'parse_account_add_character')
        content = content.replace('AccountAddCharacter_to_json', 'account_add_character_to_json')
        
        # Fix 5: Remove extra semicolons after Ok statements
        content = re.sub(r'Ok\([^)]+\);;', ');', content)
        
        if content != original_content:
            with open(rs_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rs_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rs_file}: {e}")

# Fix mod.rs imports
mod_file = generated_dir / "mod.rs"
if mod_file.exists():
    try:
        with open(mod_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the mod.rs to use correct paths
        content = content.replace('pub use generated::actions::', 'pub use actions::')
        content = re.sub(r'pub use \w+::parse_\w+;', '', content)  # Remove old function imports
        
        if content != original_content:
            with open(mod_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {mod_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {mod_file}: {e}")

print(f"Fixed {fixed_files} files total")