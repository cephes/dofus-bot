#!/usr/bin/env python3
import os
import glob

def fix_parser_syntax():
    """Fix syntax errors in all generated parser files"""
    
    # Pattern for all generated parser files
    pattern = "core/src/retroproto_parsers/generated/*.rs"
    
    files_fixed = 0
    
    for file_path in glob.glob(pattern):
        if file_path.endswith('mod.rs') or file_path.endswith('generation_report.json'):
            continue
            
        print(f"Fixing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix various common syntax issues:
            
            # 1. Extra closing braces at the end
            while content.endswith('}}'):
                content = content[:-1]
            
            # 2. Missing closing braces
            if not content.strip().endswith('}'):
                content += '\n}'
            
            # 3. Fix extra parentheses
            content = content.replace('})', '}')
            
            # 4. Fix malformed Ok() constructs
            # Replace patterns like "Ok(...)})" with "Ok(...)}"
            import re
            content = re.sub(r'Ok\(([^)]*)\}\)', r'Ok(\1)}', content)
            
            # 5. Fix unclosed struct literals
            # Look for patterns like "struct { field: value }}" and fix them
            content = re.sub(r'(\w+ \{[^}]*?)\}\}', r'\1}', content)
            
            # 6. Fix the specific issue with extra closing braces in struct construction
            # Pattern: Ok(StructName { field1: value1, field2: value2 }})
            # Should be: Ok(StructName { field1: value1, field2: value2 })
            content = re.sub(r'Ok\(\s*(\w+)\s*\{([^}]*)\}\}\)', r'Ok(\1 {\2})', content)
            
            # 7. Ensure proper comma separation
            # Fix cases where there are double commas
            content = content.replace(',,', ',')
            
            # 8. Remove trailing commas before closing braces
            content = re.sub(r',\s*}', '}', content)
            content = re.sub(r',\s*]', ']', content)
            
            if content != original_content:
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
    fix_parser_syntax()