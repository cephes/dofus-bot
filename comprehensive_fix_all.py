import os
import re
from pathlib import Path

# Comprehensive fix for all remaining syntax issues
generated_dir = Path("core/src/retroproto_parsers/generated")

total_files = 0
fixed_files = 0

for rust_file in generated_dir.rglob("*.rs"):
    total_files += 1
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Add missing semicolons after Ok() statements
        # Pattern: Ok(Struct { field: value }) followed by newline and pub fn
        content = re.sub(
            r'(Ok\(\s*\w+\s*\{[^}]*\}\s*\))(?=\s*pub\s+fn)',
            r'\1;',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 2: Escape 'type' keyword in struct fields
        content = re.sub(
            r'pub\s+type\s*:',
            'pub r#type:',
            content
        )
        
        # Fix 3: Fix Ok() statements that are missing semicolons at end of file
        content = re.sub(
            r'(Ok\(\s*\w+\s*\{[^}]*\}\s*\))(?=\s*$)',
            r'\1;',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 4: Fix broken function signatures
        content = re.sub(
            r'pub\s+fn\s+parse_\w+\s+Ok\(',
            'pub fn parse_',
            content
        )
        
        # Fix 5: Remove extra closing braces in Ok() statements
        content = re.sub(
            r'Ok\(\s*\w+\s*\{[^}]*\}\}\)\s*;',
            lambda m: m.group(0).replace('})', ')') + ';',
            content
        )
        
        # Fix 6: Ensure proper semicolons after single-line Ok() returns
        content = re.sub(
            r'(Ok\(\s*\w+\s*\{[^}]*\}\s*\))\s*pub\s+fn',
            r'\1;\n\npub fn',
            content
        )
        
        # Fix 7: Fix any remaining Ok() statements without semicolons
        lines = content.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            fixed_lines.append(line)
            if 'Ok(' in line and line.strip().endswith(')') and not line.strip().endswith(';'):
                # This is likely a missing semicolon
                fixed_lines[-1] = line + ';'
        
        content = '\n'.join(fixed_lines)
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_files += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_files} out of {total_files} files")

# Also fix the GameActions.rs file
game_actions_file = Path("core/src/retroproto_parsers/handwritten/GameActions.rs")
if game_actions_file.exists():
    try:
        with open(game_actions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the extra closing brace
        content = content.replace('Ok(GameActions { action_code, rest }})', 'Ok(GameActions { action_code, rest })')
        
        with open(game_actions_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {game_actions_file}")
    except Exception as e:
        print(f"Error processing GameActions.rs: {e}")