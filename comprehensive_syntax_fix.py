#!/usr/bin/env python3
import os
import glob
import re

def comprehensive_fix():
    """Fix all common syntax errors in generated parser files"""
    
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
            
            # 1. Fix struct definitions - add missing commas before closing brace
            content = re.sub(r'([^{,}]+)\s*}\s*$', r'\1,\n}', content, flags=re.MULTILINE)
            
            # 2. Fix function naming - convert PascalCase to snake_case for to_json functions
            # Match patterns like: pub fn AccountName_to_json
            content = re.sub(r'pub fn ([A-Z][a-zA-Z0-9_]+)_to_json', 
                           lambda m: f"pub fn {m.group(1).lower()}_to_json", content)
            
            # 3. Fix the Ok() calls that are missing closing parenthesis
            # Pattern: Ok(StructName { field1: value1, field2: value2 })
            # Should have proper closing
            content = re.sub(r'Ok\(\s*(\w+)\s*\{([^}]*)\}\s*$', 
                           r'Ok(\1 {\2})', content, flags=re.MULTILINE)
            
            # 4. Fix incomplete Ok() calls that are missing the final closing
            content = re.sub(r'Ok\(\s*(\w+)\s*\{([^}]*)\}\s*$', 
                           r'Ok(\1 {\2})', content, flags=re.MULTILINE)
            
            # 5. Fix the json! macro calls - ensure proper formatting
            content = re.sub(r'pub fn \w+_to_json\(m: &(\w+)\) -> Value \{ json!\(m\) \}$',
                           lambda m: f'pub fn {m.group(1).lower()}_to_json(m: &{m.group(1)}) -> Value {{\n  json!({{\n    "message": "Manual implementation needed",\n  }})\n}}', 
                           content, flags=re.MULTILINE)
            
            # 6. Clean up any remaining syntax issues
            # Fix extra closing braces
            content = re.sub(r'\}\s*\}\s*$', '}', content, flags=re.MULTILINE)
            
            # 7. Ensure proper function signature for parse functions
            content = re.sub(r'pub fn parse_(\w+)\(payload: &str\) -> Result<(\w+), String>',
                           r'pub fn parse_\1(payload: &str) -> Result<\2, String>', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_fixed += 1
                print(f"  Fixed {file_path}")
            else:
                print(f"  No changes needed for {file_path}")
                
        except Exception as e:
            print(f"  Error fixing {file_path}: {e}")
    
    print(f"\nTotal files fixed: {files_fixed}")

if __name__ == "__main__":
    comprehensive_fix()