#!/usr/bin/env python3
"""
Fix all incomplete parser files with missing closing braces and function endings.
"""
import os
import re
import glob

def fix_incomplete_file(filepath):
    """Fix incomplete parser files by adding missing closing braces and function endings."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if file ends abruptly without proper function closing
        lines = content.split('\n')
        
        # If file doesn't end with proper function structure, fix it
        if not content.strip().endswith('}'):
            # Look for incomplete if-else blocks
            if 'if p.is_empty()' in content and 'Ok(' in content:
                # Find the last incomplete function
                if content.count('}') < content.count('{'):
                    # Add missing closing braces and function ending
                    content += '''
    }
}

pub fn AccountAttributeGiftToCharacter_to_json(m: &AccountAttributeGiftToCharacter) -> Value {
    serde_json::json!(m)
}'''
                    # But we need to use the actual function name
                    # Extract the function name from the file
                    func_match = re.search(r'pub fn parse_(\w+)\(', content)
                    if func_match:
                        func_name = func_match.group(1)
                        # Replace the placeholder with actual function name
                        content = content.replace('AccountAttributeGiftToCharacter_to_json', f'{func_name}_to_json')
                        content = content.replace('AccountAttributeGiftToCharacter', func_name)
        
        # Fix any other common incomplete patterns
        # Pattern: Ok(Struct{}) - missing closing braces and function end
        content = re.sub(r'Ok\(\w+\{\}\)\s*$', lambda m: m.group(0) + '''
    }
}

pub fn ''' + 'TO_JSON_FUNCTION_PLACEHOLDER' + '''(m: &STRUCT_NAME_PLACEHOLDER) -> Value {
    serde_json::json!(m)
}''', content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  -> Fixed incomplete file: {filepath}")
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
    
    print(f"Checking {total_count} parser files for incomplete endings...")
    
    for filepath in parser_files:
        if fix_incomplete_file(filepath):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} incomplete parser files")

if __name__ == "__main__":
    main()