import os
import re

def fix_rust_delimiter_syntax(file_path):
    """Fix Rust delimiter issues like double braces and extra closing braces"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix double braces in Ok() constructs
        content = re.sub(r'Ok\(\{\}\}\)', 'Ok({})', content)
        
        # Fix double braces in other contexts
        content = re.sub(r'\{\{', '{', content)
        content = re.sub(r'\}\}', '}', content)
        
        # Fix extra closing braces at end of function
        content = re.sub(r'\}\s*\}\s*\n$', '\n}', content, flags=re.MULTILINE)
        
        # Fix unmatched braces by ensuring proper closure
        # Remove trailing whitespace that might cause issues
        content = content.rstrip()
        
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
                if fix_rust_delimiter_syntax(file_path):
                    fixed_count += 1
    
    print(f"\nProcessed {total_count} files, fixed {fixed_count} files")

if __name__ == "__main__":
    main()