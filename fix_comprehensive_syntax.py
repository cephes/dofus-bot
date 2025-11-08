#!/usr/bin/env python3
import os
import re

def fix_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Missing closing parentheses and braces in Ok() calls
        # Pattern: Ok(struct_name {);  -> Ok(struct_name {})
        content = re.sub(r'Ok\(\s*(\w+)\s*\{;\s*\)', r'Ok(\1 {})', content)
        
        # Fix 2: Missing closing }); for empty struct returns
        # Pattern: return Ok(struct_name {);  -> return Ok(struct_name {});
        content = re.sub(r'return\s+Ok\(\s*(\w+)\s*\{;\s*\)', r'return Ok(\1 {});', content)
        
        # Fix 3: Missing closing }) at end of if/else
        # Pattern: } else { return Ok(struct {); } -> } else { return Ok(struct {}); }
        content = re.sub(r'\}\s*else\s*\{\s*return\s+Ok\(\s*(\w+)\s*\{;\s*\)', r'} else { return Ok(\1 {});', content)
        
        # Fix 4: Fix incomplete json! macro calls
        # Pattern: serde_json::json!({  -> serde_json::json!({})
        content = re.sub(r'serde_json::json!\(\{\s*\)', r'serde_json::json!({})', content)
        
        # Fix 5: Missing closing braces in function definitions
        content = re.sub(r'pub fn \w+\(.*?\) -> .*? \{[^}]*$', lambda m: m.group(0) + '}', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    generated_dir = "core/src/retroproto_parsers/generated"
    if not os.path.exists(generated_dir):
        print(f"Directory {generated_dir} not found")
        return
    
    fixed_count = 0
    total_files = 0
    
    # Process all .rs files in the generated directory
    for filename in os.listdir(generated_dir):
        if filename.endswith('.rs'):
            file_path = os.path.join(generated_dir, filename)
            total_files += 1
            if fix_file(file_path):
                fixed_count += 1
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {fixed_count}")

if __name__ == "__main__":
    main()