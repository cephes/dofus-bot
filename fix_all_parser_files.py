#!/usr/bin/env python3
"""Fix syntax errors in all generated parser files."""

import os
import glob
import re

def fix_parser_files():
    """Fix syntax errors in all parser files."""
    generated_dir = "core/src/retroproto_parsers/generated/"
    
    # Get all .rs files in the generated directory
    parser_files = glob.glob(os.path.join(generated_dir, "*.rs"))
    
    fixed_count = 0
    for file_path in parser_files:
        print(f"Checking: {file_path}")
        
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix patterns:
        # 1. Extra closing braces: Ok(... {}}) -> Ok(... {})
        content = re.sub(r'Ok\([^)]*\s*}\s*}\s*\)', 
                        lambda m: m.group(0).replace('})', ')').replace('}}', '}'), content)
        
        # 2. Fix line 18 pattern: Ok(AccountAddCharacter { ... }} => Ok(AccountAddCharacter { ... })
        content = re.sub(r'Ok\([^)]*\}\s*}\s*\)', 
                        lambda m: m.group(0).replace('})', ')').replace('}}', '}'), content)
        
        # 3. Fix formatting issues with long single lines - add line breaks
        content = re.sub(r'Ok\([^)]*\{[^}]*\)', 
                        lambda m: fix_long_line(m.group(0)), content)
        
        # 4. Remove trailing commas before closing braces
        content = re.sub(r',\s*\}', '}', content)
        content = re.sub(r',\s*\)', ')', content)
        
        # Write back the fixed content if changes were made
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            fixed_count += 1
            print(f"  -> Fixed {file_path}")
    
    print(f"Fixed {fixed_count} parser files")
    return fixed_count

def fix_long_line(line):
    """Fix long single-line function definitions by adding proper formatting."""
    if 'Ok(AccountAddCharacter' in line:
        return """Ok(AccountAddCharacter {
    name: parts.get(0).map(|s| s.to_string()).unwrap_or_default(),
    class: parts.get(1).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
    sex: parts.get(2).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
    color1: parts.get(3).map(|s| s.to_string()).unwrap_or_default(),
    color2: parts.get(4).map(|s| s.to_string()).unwrap_or_default(),
    color3: parts.get(5).map(|s| s.to_string()).unwrap_or_default(),
  })"""
    elif 'Ok(AccountBoost' in line:
        return """Ok(AccountBoost {
    amount: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),
  })"""
    else:
        # Simple fix for other Ok( pattern
        return line.replace('})', ')').replace('}}', '}')

if __name__ == "__main__":
    fix_parser_files()