#!/usr/bin/env python3
"""
Enhanced parser file fixer for all syntax errors in generated Rust files.
"""
import os
import re
import glob
import sys

def fix_parser_file(filepath):
    """Fix syntax errors in a single parser file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix extra closing braces in function bodies
        # Pattern: Ok(...)})}) - extra closing braces
        content = re.sub(r'([)])\s*}\s*}\s*}\s*', r'\1\n  })\n}', content)
        content = re.sub(r'([)])\s*}\s*}\s*', r'\1\n  })', content)
        
        # Fix missing commas in struct fields
        # Pattern: pub field: Type}  -> pub field: Type,
        content = re.sub(r'(\w+:\s*\w+[^,\n])\s*}', r'\1,', content)
        
        # Fix extra closing braces after function calls
        # Pattern: })})  -> })
        content = re.sub(r'}\)\s*}\)\s*$', '})', content, flags=re.MULTILINE)
        
        # Fix malformed Ok() calls
        # Pattern: Ok(field: value})})  -> Ok(field: value})
        content = re.sub(r'Ok\(([^)]+)\}\s*}\s*\)', r'Ok(\1\n  })', content)
        
        # Fix struct definitions missing commas
        # Pattern: pub field: Type} -> pub field: Type,
        content = re.sub(r'pub\s+\w+:\s*\w+\s*}', lambda m: m.group(0).replace('}', ',') if m.group(0).count('}') == 1 else m.group(0), content)
        
        # Fix extra closing braces in multi-line contexts
        content = re.sub(r'(\))\s*}\s*}\s*\n\s*}', r'\1\n  })', content)
        
        # Ensure proper function closing
        content = re.sub(r'(\))\s*}\s*}\s*$', r'\1\n}', content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  -> Fixed {filepath}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"  -> Error fixing {filepath}: {e}")
        return False

def main():
    parser_files = glob.glob("core/src/retroproto_parsers/generated/*.rs")
    parser_files.extend(glob.glob("core/src/retroproto_parsers/generated/actions/*.rs"))
    
    fixed_count = 0
    total_count = len(parser_files)
    
    print(f"Checking {total_count} parser files...")
    
    for filepath in parser_files:
        if fix_parser_file(filepath):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} parser files")

if __name__ == "__main__":
    main()