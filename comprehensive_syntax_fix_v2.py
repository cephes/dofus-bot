#!/usr/bin/env python3
"""Comprehensive fix for all syntax errors in generated Rust parser files."""

import os
import re
from pathlib import Path

def fix_parser_file(file_path):
    """Fix all syntax errors in a single Rust parser file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove ALL trailing commas (most important)
        # Pattern: "}\n," -> "}\n"
        content = re.sub(r'^\},\s*$', '}', content, flags=re.MULTILINE)
        
        # Fix 2: Remove trailing commas at end of file
        lines = content.split('\n')
        while lines and lines[-1].strip() == ',':
            lines = lines[:-1]
        content = '\n'.join(lines)
        
        # Fix 3: Fix missing return statements in if blocks
        # Pattern: "    Ok(StructName {})" -> "    return Ok(StructName {});"
        content = re.sub(r'^(\s+)Ok\(([^)]+)\)\s*\{?$', r'\1return Ok(\2 {});\n}', content, flags=re.MULTILINE)
        
        # Fix 4: Remove commas after Ok() in if blocks
        content = re.sub(r'(Ok\([^)]+\)\s*)\{?\s*,?\s*$', r'\1;\n}', content, flags=re.MULTILINE)
        
        # Fix 5: Fix function definitions ending with comma
        # Pattern: "pub fn name_to_json(...) -> Value { ... }," -> "pub fn name_to_json(...) -> Value { ... }"
        content = re.sub(r'(\})\s*,\s*$', r'\1', content, flags=re.MULTILINE)
        
        # Fix 6: Fix reserved keyword "type" being used as field name
        content = re.sub(r'pub type:', 'pub type_field:', content)
        
        # Fix 7: Fix incomplete struct definitions
        content = re.sub(r'(pub struct\s+\w+\s*\{)\s*(\}\s*,?\s*)$', r'\1\n}', content)
        
        # Fix 8: Ensure all functions end with semicolon
        content = re.sub(r'pub fn\s+\w+\([^)]*\)\s*->\s*\w+\s*\{[^}]*$', 
                        lambda m: m.group(0) + '\n}', content, flags=re.MULTILINE)
        
        # Fix 9: Remove any remaining orphaned commas
        content = re.sub(r',$', '', content, flags=re.MULTILINE)
        
        # Fix 10: Fix incomplete if/else blocks
        content = re.sub(r'(\s+)Ok\([^)]+\)\s*(\{?\s*)$', r'\1return Ok(\2);\n', content)
        
        # Write back if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def create_actions_directory():
    """Create the actions directory if it doesn't exist."""
    actions_dir = Path("core/src/retroproto_parsers/generated/actions")
    if not actions_dir.exists():
        actions_dir.mkdir(parents=True, exist_ok=True)
        # Create a basic mod.rs for actions
        mod_content = """// Generated action parsers module
"""
        with open(actions_dir / "mod.rs", 'w') as f:
            f.write(mod_content)
        print(f"Created actions directory and mod.rs")

def fix_mod_rs():
    """Fix the generated/mod.rs file to remove incorrect imports."""
    mod_path = Path("core/src/retroproto_parsers/generated/mod.rs")
    if mod_path.exists():
        try:
            with open(mod_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the problematic pub use statements
            lines = content.split('\n')
            cleaned_lines = []
            skip_next = False
            for line in lines:
                if 'pub use generated::actions::' in line:
                    continue  # Skip these lines
                elif skip_next and ';' in line:
                    skip_next = False
                    continue
                else:
                    cleaned_lines.append(line)
            
            # Write back
            with open(mod_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))
            print(f"Fixed {mod_path}")
        except Exception as e:
            print(f"Error fixing mod.rs: {e}")

def main():
    """Fix all generated parser files."""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print(f"Directory {generated_dir} does not exist!")
        return
    
    # Create actions directory if missing
    create_actions_directory()
    
    # Fix mod.rs
    fix_mod_rs()
    
    # Process all .rs files in the generated directory
    fixed_count = 0
    total_count = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        total_count += 1
        if fix_parser_file(rs_file):
            fixed_count += 1
    
    print(f"\nProcessed {total_count} files, fixed {fixed_count} files")

if __name__ == "__main__":
    main()