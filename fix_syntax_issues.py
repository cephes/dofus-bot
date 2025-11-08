#!/usr/bin/env python3
import os
import re

def fix_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the specific pattern: Ok(struct_name {); -> Ok(struct_name {});
        original_content = content
        content = re.sub(r'Ok\(\s*(\w+)\s*\{;\s*\)', r'Ok(\1 {})', content)
        
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