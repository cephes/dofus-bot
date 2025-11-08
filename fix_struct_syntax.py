import os
import re

def fix_rust_struct_syntax(file_path):
    """Fix Rust struct field declarations by replacing semicolons with commas"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix struct field declarations: replace semicolons with commas
        # Pattern: field_name: Type; -> field_name: Type,
        content = re.sub(r'(\w+:\s*\w+);\s*\n', r'\1,\n', content)
        
        # Fix the last field in struct (no comma after it)
        # Pattern: field_name: Type\n} -> field_name: Type\n}
        content = re.sub(r'(\w+:\s*\w+)\n\s*\}\s*\n', r'\1\n}\n', content)
        
        # Handle empty structs
        content = re.sub(r'pub struct\s+\w+\s*\{\s*\}\s*\{', 'pub struct \\g<0>', content)
        
        # Fix double braces for empty structs
        content = re.sub(r'\{\s*\}\s*\{', '{}', content)
        
        # Write back if changed
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
    fixed_count = 0
    total_count = 0
    
    # Process all .rs files in the generated directory
    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                total_count += 1
                if fix_rust_struct_syntax(file_path):
                    fixed_count += 1
    
    print(f"\nProcessed {total_count} files, fixed {fixed_count} files")

if __name__ == "__main__":
    main()