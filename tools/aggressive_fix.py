#!/usr/bin/env python3
"""
Aggressive syntax fix for Rust parse functions - addresses the most critical build errors.
"""

import re
import pathlib
import json

# Constants
ROOT = pathlib.Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ACT_DIR = GEN_DIR / "actions"
CACHE_FILE = ROOT / "tools" / "_cache" / "go_structs.json"

def fix_parse_function_syntax_aggressive():
    """Aggressively fix parse function syntax by rebuilding malformed struct creation."""
    print("Aggressively fixing parse function syntax...")
    changes = 0
    
    all_rust_files = list(GEN_DIR.glob("*.rs")) + list(ACT_DIR.glob("*.rs"))
    
    for rust_file in all_rust_files:
        if rust_file.name in ["mod.rs", "mod.rs.bak"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            original_content = content
            
            # Find all parse functions and fix their syntax
            parse_fn_pattern = r'(pub\s+fn\s+(parse_\w+)\s*\([^)]*\)\s*->\s*Result\s*<[^>]*>\s*\{[^}]*Ok\([^)]*\s*\{[^}]*\}[^}]*\}[^}]*\}[^}]*\})'
            
            def fix_parse_function(match):
                full_match = match.group(0)
                
                # Extract function name
                fn_name_match = re.search(r'pub\s+fn\s+(parse_\w+)', full_match)
                if not fn_name_match:
                    return full_match
                
                fn_name = fn_name_match.group(1)
                struct_name = fn_name.replace('parse_', '')
                
                # Extract existing field assignments that are syntactically correct
                field_assignments = re.findall(r'(\w+:\s*[^,}]+(?:,\s*)?)', full_match)
                valid_fields = []
                
                for field_assign in field_assignments:
                    # Check if this looks like a valid field assignment
                    if ':' in field_assign and not field_assign.strip().endswith('}') and not 'Default::default()Default::default()' in field_assign:
                        valid_fields.append(field_assign.strip().rstrip(','))
                
                # If we have valid fields, build a clean struct creation
                if valid_fields:
                    clean_field_list = ',\n        '.join(valid_fields)
                    if not clean_field_list.endswith(','):
                        clean_field_list += ','
                    
                    # Replace the malformed struct creation
                    fixed_fn = re.sub(
                        r'Ok\([^)]*\s*\{[^}]*\}[^}]*\}[^}]*\}[^}]*\)',
                        f'Ok({struct_name} {{\n        {clean_field_list}\n    }})',
                        full_match
                    )
                    return fixed_fn
                else:
                    # No valid fields, use minimal struct creation
                    minimal_fn = re.sub(
                        r'Ok\([^)]*\s*\{[^}]*\}[^}]*\}[^}]*\}[^}]*\)',
                        f'Ok({struct_name}::default())',
                        full_match
                    )
                    return minimal_fn
            
            # Apply the fix
            content = re.sub(parse_fn_pattern, fix_parse_function, content, flags=re.MULTILINE | re.DOTALL)
            
            # Also fix any remaining duplicate field patterns
            content = re.sub(r'(\w+:\s*[^,}]+),\s*\1', r'\1', content)
            
            # Fix incomplete field assignments
            content = re.sub(r'(\w+:\s*Default::default\(\))(\w+:\s*Default::default\(\))', r'\1, \2', content)
            
            # If content changed, write it back
            if content != original_content:
                rust_file.write_text(content, encoding='utf-8')
                changes += 1
                print(f"  Fixed syntax in {rust_file.name}")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def fix_missing_fields_from_go():
    """Add missing fields based on Go struct definitions."""
    print("Adding missing fields from Go definitions...")
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
                    current_field_names = set()
                    field_pattern = r'pub\s+(\w+)\s*:\s*([^,}]+)'
                    for field_match in re.finditer(field_pattern, struct_body):
                        field_name = field_match.group(1)
                        current_field_names.add(field_name)
                    
                    # Check for missing fields
                    missing_rust_names = set()
                    for go_field_name in go_field_names:
                        rust_field_name = normalize_field_name(go_field_name)
                        if rust_field_name not in current_field_names:
                            missing_rust_names.add(rust_field_name)
                    
                    # Add missing fields
                    if missing_rust_names:
                        # Determine field types from Go
                        new_field_defs = []
                        for go_field in go_struct['fields']:
                            rust_field_name = normalize_field_name(go_field['name'])
                            if rust_field_name in missing_rust_names:
                                field_type = map_go_type_to_rust(go_field['type'])
                                new_field_defs.append(f"  pub {rust_field_name}: {field_type},")
                        
                        if new_field_defs:
                            # Insert new fields before closing brace
                            new_content = (
                                content[:struct_end] + 
                                '\n' + '\n'.join(new_field_defs) + '\n' +
                                content[struct_end:]
                            )
                            
                            # Also update parse function to initialize new fields
                            parse_fn_pattern = rf'pub\s+fn\s+(parse_{re.escape(struct_name)})\s*\([^)]*\)\s*->\s*Result\s*<[^>]*>'
                            parse_match = re.search(parse_fn_pattern, new_content)
                            
                            if parse_match:
                                # Add field initializations to parse function
                                field_inits = []
                                for rust_field_name in missing_rust_names:
                                    field_inits.append(f"{rust_field_name}: Default::default()")
                                
                                if field_inits:
                                    # Find struct creation in parse function and add new field inits
                                    struct_creation_pattern = rf'Ok\({re.escape(struct_name)}\s*\{{([^}}]*)\}}'
                                    struct_creation_match = re.search(struct_creation_pattern, new_content)
                                    
                                    if struct_creation_match:
                                        existing_fields = struct_creation_match.group(1)
                                        new_field_inits_str = ',\n        '.join(field_inits)
                                        updated_struct_creation = f"Ok({struct_name} {{\n        {existing_fields}\n        {new_field_inits_str}\n    }})"
                                        
                                        new_content = new_content[:struct_creation_match.start()] + updated_struct_creation + new_content[struct_creation_match.end():]
                            
                            rust_file.write_text(new_content, encoding='utf-8')
                            changes += 1
                            print(f"  Added {len(missing_rust_names)} missing fields to {struct_name}")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def normalize_field_name(name: str) -> str:
    """Convert Go/PascalCase field name to Rust snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()

def map_go_type_to_rust(go_type: str) -> str:
    """Map Go type to Rust type."""
    # Remove potential package prefixes and clean up
    clean_type = go_type.split('.')[-1] if '.' in go_type else go_type
    clean_type = clean_type.split(']')[-1]  # Remove array indicators
    clean_type = clean_type.strip()
    
    # Type mapping
    type_map = {
        'int': 'i64',
        'int32': 'i64', 
        'int64': 'i64',
        'string': 'String',
        'bool': 'bool',
        'rune': 'i64',
        '[]int': 'Vec<i64>',
        '[]int32': 'Vec<i64>',
        '[]int64': 'Vec<i64>',
        '[]string': 'Vec<String>',
        '[]bool': 'Vec<bool>',
    }
    
    if clean_type in type_map:
        return type_map[clean_type]
    
    # Slice types
    if clean_type.startswith('[]'):
        base_type = clean_type[2:]
        rust_base = map_go_type_to_rust(base_type)
        if rust_base != 'String':
            return f"Vec<{rust_base}>"
        return "Vec<String>"
    
    # Default fallback
    return "String"

def fix_registry_imports():
    """Fix missing imports in registry.rs."""
    print("Fixing registry imports...")
    
    registry_file = ROOT / "core" / "src" / "retroproto_parsers" / "registry.rs"
    if not registry_file.exists():
        print("  Registry file not found")
        return 0
    
    try:
        content = registry_file.read_text(encoding='utf-8')
        
        # Find all action parsers that need imports
        action_parsers = []
        action_pattern = r'match\s+(parse_(GameAction|CliAction)_(\w+))'
        for match in re.finditer(action_pattern, content):
            action_parsers.append(match.group(1))
        
        if action_parsers:
            # Remove duplicate imports
            existing_imports = re.findall(r'use\s+crate::retroproto_parsers::generated::actions::(\w+::\w+);', content)
            
            # Add missing imports
            new_imports = []
            for parser in action_parsers:
                if parser not in existing_imports:
                    module_name = parser.replace('parse_', '')
                    import_line = f"use crate::retroproto_parsers::generated::actions::{module_name};"
                    new_imports.append(import_line)
            
            if new_imports:
                # Insert imports after the existing generated imports
                import_section_end = content.find('\nuse crate::retroproto_parsers::handwritten::GameActions;')
                if import_section_end != -1:
                    insert_pos = import_section_end + 1
                    new_import_section = '\n'.join(new_imports) + '\n'
                    content = content[:insert_pos] + new_import_section + content[insert_pos:]
                    
                    registry_file.write_text(content, encoding='utf-8')
                    print(f"  Added {len(new_imports)} missing action imports")
                    return len(new_imports)
        
        print("  No action imports needed")
        return 0
        
    except Exception as e:
        print(f"Error fixing registry imports: {e}")
        return 0

def main():
    """Run the aggressive fix."""
    print("Starting aggressive syntax fix...")
    print("-" * 50)
    
    total_changes = 0
    
    # Fix parse function syntax
    changes1 = fix_parse_function_syntax_aggressive()
    total_changes += changes1
    
    # Add missing fields from Go
    changes2 = fix_missing_fields_from_go()
    total_changes += changes2
    
    # Fix registry imports
    changes3 = fix_registry_imports()
    total_changes += changes3
    
    print("-" * 50)
    print(f"Aggressive fix completed: {total_changes} changes made")
    
    # Test build
    print("Testing build...")
    try:
        import subprocess
        result = subprocess.run([
            "cargo", "build", "--release", "-p", "dofus-core"
        ], capture_output=True, text=True, cwd=str(ROOT / "core"))
        
        if result.returncode == 0:
            print("SUCCESS: Build completed successfully!")
            return True
        else:
            print(f"FAILED: Build failed with {result.returncode} errors")
            print("First 30 lines of errors:")
            error_lines = result.stderr.split('\n')[:30]
            for line in error_lines:
                print(f"  {line}")
            return False
    except Exception as e:
        print(f"Error running build: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)