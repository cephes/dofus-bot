#!/usr/bin/env python3
"""
Fix function naming mismatch in action parsers.
The action files have parse_game_action_1 but registry expects parse_GameAction_1
"""

import os
import re

def fix_action_files():
    """Fix function names in action parser files"""
    actions_dir = "core/src/retroproto_parsers/generated/actions"
    
    # Mapping of snake_case to PascalCase function names
    function_mappings = {
        'parse_game_action_': 'parse_GameAction_',
        'parse_cli_action_': 'parse_CliAction_',
        'game_action_': 'GameAction_',
        'cli_action_': 'CliAction_',
    }
    
    fixed_count = 0
    
    for filename in os.listdir(actions_dir):
        if filename.endswith('.rs') and filename != 'mod.rs':
            filepath = os.path.join(actions_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply the function name mappings
            for snake_name, pascal_name in function_mappings.items():
                # Replace function definitions
                content = re.sub(
                    rf'pub fn {snake_name}(\d+)',
                    f'pub fn {pascal_name}\\1',
                    content
                )
                # Replace function calls in to_json functions
                content = re.sub(
                    rf'{snake_name}(\d+)\(',
                    f'{pascal_name}\\1(',
                    content
                )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed function names in {filename}")
                fixed_count += 1
    
    print(f"Fixed {fixed_count} action files")
    return fixed_count

if __name__ == "__main__":
    fix_action_files()