#!/usr/bin/env python3
"""
Fix Rust reserved keywords in generated parser files

Escapes reserved keywords like 'type' to 'r#type' to avoid compilation errors
"""

import os
import re
from pathlib import Path

# Reserved Rust keywords that can't be used as field names
RESERVED_KEYWORDS = [
    'as', 'async', 'await', 'break', 'const', 'continue', 'crate', 'dyn', 'else', 'enum', 
    'extern', 'false', 'fn', 'for', 'if', 'impl', 'in', 'let', 'loop', 'match', 'mod', 
    'move', 'mut', 'pub', 'ref', 'return', 'self', 'Self', 'static', 'struct', 'super', 
    'trait', 'true', 'type', 'unsafe', 'use', 'where', 'while'
]

def fix_reserved_keywords(content: str) -> str:
    """Fix reserved keywords in field declarations and usage"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Fix field declarations like: pub type: String,
        field_decl_match = re.search(r'\b(pub\s+)?(\w+):\s+(\w+)', line)
        if field_decl_match and field_decl_match.group(2) in RESERVED_KEYWORDS:
            keyword = field_decl_match.group(2)
            prefix = field_decl_match.group(1) or ''
            field_name = field_decl_match.group(2)
            field_type = field_decl_match.group(3)
            
            # Replace with escaped version
            line = line.replace(
                f"{prefix}{field_name}: {field_type}",
                f"{prefix}r#{field_name}: {field_type}"
            )
            print(f"Fixed field declaration: {field_name} -> r#{field_name}")
        
        # Fix variable usage like: let type = ...
        var_usage_match = re.search(r'\blet\s+(\w+)\s*=', line)
        if var_usage_match and var_usage_match.group(1) in RESERVED_KEYWORDS:
            keyword = var_usage_match.group(1)
            line = line.replace(f"let {keyword} =", f"let r#{keyword} =")
            print(f"Fixed variable usage: {keyword} -> r#{keyword}")
        
        # Fix struct constructor usage: type,
        constructor_match = re.search(r'\b(\w+),', line)
        if (constructor_match and 
            constructor_match.group(1) in RESERVED_KEYWORDS and
            'let ' not in line and  # Not a variable declaration
            'pub ' not in line):     # Not a field declaration
            
            keyword = constructor_match.group(1)
            line = line.replace(f"{keyword},", f"r#{keyword},")
            print(f"Fixed constructor usage: {keyword} -> r#{keyword}")
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def main():
    """Fix all generated parser files"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found!")
        return
    
    fixed_files = []
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
            
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file needs fixing
            needs_fixing = any(f"pub {kw}:" in content or f"let {kw} =" in content for kw in RESERVED_KEYWORDS)
            
            if needs_fixing:
                fixed_content = fix_reserved_keywords(content)
                with open(rs_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                fixed_files.append(str(rs_file))
                print(f"Fixed: {rs_file}")
        
        except Exception as e:
            print(f"Error processing {rs_file}: {e}")
    
    print(f"\nFixed {len(fixed_files)} files:")
    for file in fixed_files:
        print(f"  {file}")

if __name__ == "__main__":
    main()