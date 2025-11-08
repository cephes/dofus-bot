#!/usr/bin/env python3
import os
import glob

def fix_gameaction_files():
    """Fix syntax errors in all GameAction files"""
    
    # Pattern for GameAction files
    pattern = "core/src/retroproto_parsers/generated/actions/GameAction_*.rs"
    
    files_fixed = 0
    
    for file_path in glob.glob(pattern):
        print(f"Fixing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the extra closing brace at the end
            if content.endswith('}}'):
                content = content[:-1]  # Remove one closing brace
                
                # Also ensure proper ending
                if not content.strip().endswith('}'):
                    content += '\n}'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_fixed += 1
                print(f"  Fixed {file_path}")
            else:
                print(f"  No fix needed for {file_path}")
                
        except Exception as e:
            print(f"  Error fixing {file_path}: {e}")
    
    print(f"\nFixed {files_fixed} GameAction files")
    
    # Now fix CliAction files
    cli_pattern = "core/src/retroproto_parsers/generated/actions/CliAction_*.rs"
    
    for file_path in glob.glob(cli_pattern):
        print(f"Fixing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the extra closing brace at the end
            if content.endswith('}}'):
                content = content[:-1]  # Remove one closing brace
                
                # Also ensure proper ending
                if not content.strip().endswith('}'):
                    content += '\n}'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_fixed += 1
                print(f"  Fixed {file_path}")
            else:
                print(f"  No fix needed for {file_path}")
                
        except Exception as e:
            print(f"  Error fixing {file_path}: {e}")
    
    print(f"\nTotal files fixed: {files_fixed}")

if __name__ == "__main__":
    fix_gameaction_files()