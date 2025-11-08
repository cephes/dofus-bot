#!/usr/bin/env python3
"""
Fix all parser files that are missing function closing and return statement
"""

from pathlib import Path

def add_function_closing(content: str) -> str:
    """Add missing function closing and return statement"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # Look for the end of struct creation line
        if line.strip() == '};' and i > 0 and 'let result = ' in fixed_lines[i-1]:
            # Add return statement and function closing
            fixed_lines.append('    Ok(result)')
            fixed_lines.append('}')
            break
    
    return '\n'.join(fixed_lines)

def fix_single_file(file_path: Path) -> bool:
    """Fix a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if the file doesn't end with a closing brace
        if not content.strip().endswith('}'):
            content = add_function_closing(content)
            
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
    """Fix all files that need function closing"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    fixed_files = 0
    
    for rs_file in generated_dir.rglob("*.rs"):
        if rs_file.name == "mod.rs":
            continue
        
        try:
            with open(rs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the file needs fixing
            if 'let result = ' in content and not content.strip().endswith('}'):
                if fix_single_file(rs_file):
                    fixed_files += 1
        except Exception as e:
            print(f"Error checking {rs_file}: {e}")
    
    print(f"\nFixed {fixed_files} files with missing function closing")

if __name__ == "__main__":
    main()