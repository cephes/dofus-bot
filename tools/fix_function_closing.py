#!/usr/bin/env python3
"""
Fix missing function body closing - add the return statement and function closing
"""

from pathlib import Path

def fix_function_closing(content: str) -> str:
    """Add missing function body closing"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # If this is the last line of the function (line ending with };), 
        # add the return statement and function closing
        if line.strip() == '};' and i > 0 and 'let result = ' in fixed_lines[i-1]:
            # This is the end of struct creation, add return and function closing
            fixed_lines.append('    Ok(result)')
            fixed_lines.append('}')
            fixed_lines.append('')
            break
    
    return '\n'.join(fixed_lines)

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if the function is missing closing
        if not content.strip().endswith('}'):
            content = fix_function_closing(content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed function closing: {file_path}")
                return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all files with missing function closing"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the function is missing closing
            lines = content.split('\n')
            if lines and not lines[-1].strip() == '}':
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with missing function closing")

if __name__ == "__main__":
    main()