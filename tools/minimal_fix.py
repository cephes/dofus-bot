#!/usr/bin/env python3
"""
Minimal fix for Rust build errors - removes duplicates and fixes syntax issues.
"""

import re
import pathlib
import json
from typing import Dict, List, Tuple, Any

# Constants
ROOT = pathlib.Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ACT_DIR = GEN_DIR / "actions"
CACHE_FILE = ROOT / "tools" / "_cache" / "go_structs.json"

def fix_duplicate_derives():
    """Remove duplicate derive statements that cause conflicts."""
    print("Fixing duplicate derive statements...")
    changes = 0
    
    for rust_file in list(GEN_DIR.glob("*.rs")) + list(ACT_DIR.glob("*.rs")):
        if rust_file.name in ["mod.rs", "mod.rs.bak"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            
            # Count derive statements
            derive_matches = re.findall(r'#\[derive\([^)]*\)\]', content)
            if len(derive_matches) > 1:
                # Keep only the first one, remove others
                first_derive = derive_matches[0]
                # Remove all derive statements
                content = re.sub(r'#\[derive\([^)]*\)\]', '', content)
                # Add back only the first one before the struct
                struct_match = re.search(r'(pub\s+struct\s+\w+\s*\{)', content)
                if struct_match:
                    content = content[:struct_match.start()] + first_derive + '\n' + content[struct_match.start():]
                    rust_file.write_text(content, encoding='utf-8')
                    changes += 1
                    print(f"  Fixed {rust_file.name}: removed {len(derive_matches)-1} duplicate derives")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def fix_parse_function_syntax():
    """Fix parse function syntax errors by removing duplicate field assignments."""
    print("Fixing parse function syntax errors...")
    changes = 0
    
    for rust_file in list(GEN_DIR.glob("*.rs")) + list(ACT_DIR.glob("*.rs")):
        if rust_file.name in ["mod.rs", "mod.rs.bak"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            original_content = content
            
            # Fix duplicate field assignments in parse functions
            # Pattern: field: Default::default(), field: Default::default()
            pattern = r'(\w+:\s*Default::default\(\),\s*\w+:\s*Default::default\(\))'
            replacement = r'\1'  # Keep only the first occurrence
            content = re.sub(pattern, replacement, content)
            
            # Fix struct creation patterns
            # Look for patterns like: Ok(StructName { ... })
            # Remove duplicate field assignments in struct literals
            struct_pattern = r'(Ok\([^)]*\s*\{[^}]*)((?:,\s*\w+:\s*Default::default\(\))+)([^}]*\}[^)]*\))'
            
            def fix_struct_duplicates(match):
                prefix = match.group(1)
                fields = match.group(2)
                suffix = match.group(3)
                
                # Split fields and remove duplicates
                field_list = [f.strip() for f in fields.split(',')]
                unique_fields = []
                seen = set()
                
                for field in field_list:
                    if field and field not in seen:
                        unique_fields.append(field)
                        seen.add(field)
                
                return prefix + (', '.join(unique_fields) if unique_fields else '') + suffix
            
            content = re.sub(struct_pattern, fix_struct_duplicates, content, flags=re.MULTILINE | re.DOTALL)
            
            # If content changed, write it back
            if content != original_content:
                rust_file.write_text(content, encoding='utf-8')
                changes += 1
                print(f"  Fixed syntax in {rust_file.name}")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def fix_field_name_conflicts():
    """Fix field name conflicts by checking Go structs for actual field names."""
    print("Checking for field name conflicts...")
    changes = 0
    
    # Load Go struct cache
    go_structs = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                by_name = data.get('by_name', {})
                for struct_name, struct_list in by_name.items():
                    if isinstance(struct_list, list) and struct_list:
                        go_structs[struct_name] = struct_list[0]
                    elif isinstance(struct_list, dict):
                        go_structs[struct_name] = struct_list
        except Exception as e:
            print(f"Failed to load Go struct cache: {e}")
            return changes
    
    for rust_file in GEN_DIR.glob("*.rs"):
        if rust_file.name in ["mod.rs", "mod.rs.bak"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            struct_name = rust_file.stem
            
            if struct_name in go_structs:
                go_struct = go_structs[struct_name]
                go_field_names = {f['name'] for f in go_struct['fields']}
                
                # Find struct in content
                struct_match = re.search(r'pub\s+struct\s+\w+\s*\{', content)
                if struct_match:
                    struct_start = content.find('{', struct_match.end())
                    brace_count = 0
                    struct_end = struct_start
                    for i, char in enumerate(content[struct_start:], struct_start):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                struct_end = i
                                break
                    
                    struct_body = content[struct_start+1:struct_end]
                    
                    # Parse current fields
                    current_fields = {}
                    field_pattern = r'pub\s+(\w+)\s*:\s*([^,}]+)'
                    for field_match in re.finditer(field_pattern, struct_body):
                        field_name = field_match.group(1)
                        field_type = field_match.group(2).strip()
                        current_fields[field_name] = field_type
                    
                    # Check for incorrect field names
                    rust_field_names = {f['name'] for f in current_fields}
                    expected_rust_names = {normalize_field_name(go_name) for go_name in go_field_names}
                    
                    if rust_field_names != expected_rust_names:
                        # Find mismatched fields
                        missing = expected_rust_names - rust_field_names
                        extra = rust_field_names - expected_rust_names
                        
                        if missing or extra:
                            print(f"  {struct_name}: expected {expected_rust_names}, found {rust_field_names}")
                            print(f"    Missing: {missing}, Extra: {extra}")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def normalize_field_name(name: str) -> str:
    """Convert Go/PascalCase field name to Rust snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()

def main():
    """Run the minimal fix."""
    print("Starting minimal build fix...")
    print("-" * 50)
    
    total_changes = 0
    
    # Fix duplicate derives
    changes1 = fix_duplicate_derives()
    total_changes += changes1
    
    # Fix parse function syntax
    changes2 = fix_parse_function_syntax()
    total_changes += changes2
    
    # Check field name conflicts
    changes3 = fix_field_name_conflicts()
    total_changes += changes3
    
    print("-" * 50)
    print(f"Minimal fix completed: {total_changes} files modified")
    
    # Test build
    print("Testing build...")
    try:
        import subprocess
        result = subprocess.run([
            "cargo", "build", "--release", "-p", "dofus-core"
        ], capture_output=True, text=True, cwd=str(ROOT / "core"))
        
        if result.returncode == 0:
            print("✅ Build successful!")
            return True
        else:
            print(f"❌ Build failed with {result.returncode}")
            print("First 20 lines of error:")
            print('\n'.join(result.stderr.split('\n')[:20]))
            return False
    except Exception as e:
        print(f"Error running build: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)