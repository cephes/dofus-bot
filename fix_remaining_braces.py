import os
import re

def fix_remaining_braces(file_path):
    """Fix remaining brace issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove extra empty lines and trailing braces
        lines = content.split('\n')
        fixed_lines = []
        brace_count = 0
        in_function = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines that might contain stray characters
            if not stripped:
                fixed_lines.append(line)
                continue
            
            # Count opening and closing braces
            brace_count += stripped.count('{')
            brace_count -= stripped.count('}')
            
            # Fix specific patterns
            if 'return Ok(' in stripped and '});' in stripped:
                line = re.sub(r'return Ok\(([^)]+)\}\);', r'return Ok(\1);', line)
            if 'return Ok(' in stripped and '}' in stripped and ');' not in stripped:
                line = re.sub(r'return Ok\(([^}]+)\}\s*\n\s*\}', r'return Ok(\1)\n}', line)
            
            fixed_lines.append(line)
        
        # Remove any trailing empty braces at the very end
        while fixed_lines and fixed_lines[-1].strip() == '}':
            fixed_lines.pop()
        
        # Ensure we end with just one closing brace for the function
        content = '\n'.join(fixed_lines)
        
        # Add final closing brace if missing
        if not content.strip().endswith('}'):
            content += '\n}'
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed braces: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    generated_dir = "core/src/retroproto_parsers/generated"
    fixed_count = 0
    
    # Process all .rs files in the generated directory
    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                if fix_remaining_braces(file_path):
                    fixed_count += 1
    
    print(f"Fixed braces in {fixed_count} files")

if __name__ == "__main__":
    main()