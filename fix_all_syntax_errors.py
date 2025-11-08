#!/usr/bin/env python3
import os
import re

def fix_all_files():
    generated_dir = "core/src/retroproto_parsers/generated"
    if not os.path.exists(generated_dir):
        print(f"Directory {generated_dir} not found")
        return
    
    fixed_files = []
    total_files = 0
    
    for filename in os.listdir(generated_dir):
        if filename.endswith('.rs') and filename != 'mod.rs':
            file_path = os.path.join(generated_dir, filename)
            total_files += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix 1: Missing semicolon after Ok() call
                content = re.sub(r'\)\s*\n\s*pub\s+fn', r');\n\npub fn', content)
                
                # Fix 2: Missing closing parentheses and braces
                content = re.sub(r'Ok\(\s*(\w+)\s*\{\s*$', r'Ok(\1 {})', content, flags=re.MULTILINE)
                
                # Fix 3: Incomplete json! macro calls
                content = re.sub(r'serde_json::json!\(\{\s*$', 'serde_json::json!({})', content, flags=re.MULTILINE)
                
                # Fix 4: Missing closing brace for json function
                content = re.sub(r'Value\s*\{\s*$', 'Value {}', content, flags=re.MULTILINE)
                
                # Fix 5: Add missing closing braces at end of files
                lines = content.split('\n')
                if lines and not lines[-1].strip() == '}':
                    lines.append('}')
                    content = '\n'.join(lines)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_files.append(filename)
                    print(f"Fixed: {filename}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {len(fixed_files)}")
    if fixed_files:
        print(f"Fixed files: {', '.join(fixed_files)}")

if __name__ == "__main__":
    fix_all_files()