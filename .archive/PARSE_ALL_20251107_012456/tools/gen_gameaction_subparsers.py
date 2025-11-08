#!/usr/bin/env python3
"""
GameAction Subparser Generator

This tool discovers GameAction struct definitions from Go sources and generates
corresponding Rust parser submodules for fully typed per-Action payload parsing.

Discovery logic:
- Scans third_party/retroproto/msgsvr/ for Go files
- Finds GameAction struct definitions (GameActionsActionMovement, etc.)
- Maps action types to codes using GameActionType enum
- Generates Rust equivalent structs with parse functions
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class GoTypeMapper:
    """Maps Go types to Rust equivalents"""
    
    @staticmethod
    def map_field_type(go_type: str, field_name: str) -> str:
        """Map Go field type to Rust type"""
        # Remove package prefixes
        go_type = go_type.split('.')[-1]
        
        type_mapping = {
            'int': 'i64',
            'int8': 'i8',
            'int16': 'i16', 
            'int32': 'i32',
            'int64': 'i64',
            'uint': 'u64',
            'uint8': 'u8',
            'uint16': 'u16',
            'uint32': 'u32',
            'uint64': 'u64',
            'float32': 'f32',
            'float64': 'f64',
            'string': 'String',
            'bool': 'bool',
            'rune': 'char',
            '[]byte': 'Vec<u8>',
            '[]string': 'Vec<String>',
        }
        
        # Handle array/slice types
        if go_type.startswith('[]'):
            inner_type = GoTypeMapper.map_field_type(go_type[2:], field_name)
            return f'Vec<{inner_type}>'
        
        # Handle complex types from the schema
        if 'CommonDirAndCell' in go_type:
            return 'Vec<(u8, u16, u8)>'  # Simplified representation
        
        return type_mapping.get(go_type, go_type)

class GameActionSubparserGenerator:
    def __init__(self,
                 go_source_dir: str = "third_party/retroproto/msgsvr",
                 rust_output_dir: str = "core/src/retroproto_parsers/generated",
                 actions_module_file: str = "core/src/retroproto_parsers/generated/actions/mod.rs"):
        self.go_source_dir = Path(go_source_dir)
        self.rust_output_dir = Path(rust_output_dir)
        self.actions_module_file = Path(actions_module_file)
        self.actions_dir = self.rust_output_dir / "actions"
        self.generated_files = []
        self.action_mapping = {}
        
    def discover_go_structs(self) -> Dict[str, Dict]:
        """Discover GameAction struct definitions from Go sources"""
        structs = {}
        
        # Load the main gameactions.go file
        gameactions_file = self.go_source_dir / "gameactions.go"
        if not gameactions_file.exists():
            print(f"Warning: {gameactions_file} not found")
            return structs
            
        with open(gameactions_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find struct definitions
        struct_pattern = r'type (GameActionsAction\w+) struct\s*\{([^}]+)\}'
        matches = re.findall(struct_pattern, content, re.MULTILINE | re.DOTALL)
        
        for struct_name, fields_content in matches:
            # Parse field definitions
            field_pattern = r'(\w+)\s+(\w+)'
            fields = {}
            
            for field_match in re.finditer(field_pattern, fields_content):
                field_name, field_type = field_match.groups()
                # Normalize field names for Rust (camelCase to snake_case)
                rust_field_name = re.sub(r'([A-Z])', r'_\1', field_name).lower().lstrip('_')
                if rust_field_name in ['type', 'match', 'ref', 'self', 'box', 'use']:
                    rust_field_name = f"{rust_field_name}_field"
                    
                fields[rust_field_name] = GoTypeMapper.map_field_type(field_type, field_name)
                
            structs[struct_name] = {
                'fields': fields,
                'action_code': self._get_action_code(struct_name),
                'go_struct_name': struct_name
            }
            
        return structs
    
    def _get_action_code(self, struct_name: str) -> Optional[int]:
        """Map Go struct name to action code based on GameActionType enum"""
        action_mapping = {
            'GameActionsActionMovement': 1,        # Movement
            'GameActionsActionLoadGameMap': 2,     # LoadGameMap  
            'GameActionsActionChallenge': 900,     # Challenge
            'GameActionsActionChallengeAccept': 901, # ChallengeAccept
            'GameActionsActionChallengeRefuse': 902, # ChallengeRefuse
            'GameActionsActionChallengeJoin': 903, # ChallengeJoin
        }
        return action_mapping.get(struct_name)
    
    def generate_rust_struct(self, struct_name: str, struct_def: Dict) -> str:
        """Generate Rust struct and parser function"""
        fields = struct_def['fields']
        action_code = struct_def['action_code']
        rust_struct_name = f"GameAction_{action_code}"
        
        # Generate field declarations
        field_decls = []
        for field_name, field_type in fields.items():
            field_decls.append(f"    pub {field_name}: {field_type},")
        
        fields_str = "\n".join(field_decls) if field_decls else "    // No fields"
        
        # Generate parsing logic
        parse_logic = self._generate_parse_logic(struct_name, struct_def, action_code)
        
        return f'''// AUTO-GENERATED GameAction subparser for action code {action_code}
// Source: {struct_def['go_struct_name']} from Go definitions

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct {rust_struct_name} {{
{fields_str}
}}

pub fn parse_{rust_struct_name}(payload: &str) -> Result<{rust_struct_name}, String> {{
{parse_logic}
}}
'''
    
    def _generate_parse_logic(self, struct_name: str, struct_def: Dict, action_code: int) -> str:
        """Generate parsing logic for the struct"""
        fields = struct_def['fields']
        rust_struct_name = f"GameAction_{action_code}"
        
        if not fields:
            return f"    Ok({rust_struct_name}::default())"
        
        # Split payload by semicolons
        parts_lines = []
        parts_lines.append("    let parts: Vec<&str> = payload.split(';').collect();")
        parts_lines.append(f"    let mut m = {rust_struct_name}::default();")
        parts_lines.append("")
        parts_lines.append("    // Parse fields from semicolon-separated payload")
        parts_lines.append("    let mut part_idx = 0;")
        
        # Generate field assignments with safe parsing
        for i, (field_name, field_type) in enumerate(fields.items()):
            parts_lines.append(f"    if part_idx < parts.len() {{")
            parts_lines.append(f"        let part = parts[part_idx].trim();")
            parts_lines.append(f"        if !part.is_empty() {{")
            
            if 'Vec<' in field_type:
                # Handle Vec types - split by commas or other delimiters
                parts_lines.append(f"            m.{field_name} = part.split(',').map(|s| s.trim().parse().unwrap_or_default()).collect();")
            elif field_type in ['i64', 'i32', 'i16', 'i8', 'u64', 'u32', 'u16', 'u8']:
                parts_lines.append(f"            m.{field_name} = part.parse().unwrap_or(0);")
            elif field_type == 'String':
                parts_lines.append(f"            m.{field_name} = part.to_string();")
            elif field_type == 'bool':
                parts_lines.append(f"            m.{field_name} = part.parse().unwrap_or(false);")
            elif field_type == 'char':
                parts_lines.append(f"            m.{field_name} = part.chars().next().unwrap_or('\\0');")
            else:
                parts_lines.append(f"            // TODO: Handle custom type {field_type}")
                parts_lines.append(f"            // m.{field_name} = part.parse().unwrap_or_default();")
            
            parts_lines.append(f"        }}")
            parts_lines.append(f"        part_idx += 1;")
            parts_lines.append(f"    }}")
            parts_lines.append("")
        
        parts_lines.append("    Ok(m)")
        
        return "\n".join(parts_lines)
    
    def write_struct_file(self, struct_name: str, struct_def: Dict) -> Path:
        """Write generated Rust struct to file"""
        rust_struct_name = f"GameAction_{struct_def['action_code']}"
        file_path = self.actions_dir / f"{rust_struct_name}.rs"
        
        content = self.generate_rust_struct(struct_name, struct_def)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        self.generated_files.append(str(file_path))
        return file_path
    
    def update_actions_module(self, structs: Dict[str, Dict]):
        """Update the actions.rs module file to include new subparsers"""
        use_lines = []
        export_lines = []
        
        for struct_name, struct_def in structs.items():
            action_code = struct_def['action_code']
            if action_code is not None:
                rust_struct_name = f"GameAction_{action_code}"
                use_lines.append(f"pub mod {rust_struct_name};")
                use_lines.append(f"pub use {rust_struct_name}::{rust_struct_name};")
                use_lines.append(f"pub use {rust_struct_name}::parse_{rust_struct_name};")
        
        # Generate module content
        module_content = f'''// AUTO-GENERATED GameAction subparsers module
// This module contains individual GameAction parsers

{chr(10).join(use_lines)}

// Note: Additional GameAction variants will be added as their corresponding
// Go struct definitions become available
'''
        
        with open(self.actions_module_file, 'w', encoding='utf-8') as f:
            f.write(module_content)
    
    def ensure_actions_directory(self):
        """Ensure the actions directory exists"""
        self.actions_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mod.rs for the actions subdirectory
        mod_rs = self.actions_dir / "mod.rs"
        if not mod_rs.exists():
            with open(mod_rs, 'w', encoding='utf-8') as f:
                f.write("// AUTO-GENERATED GameAction subparsers\n// Individual action parsers are organized as submodules\n\n")
    
    def generate(self) -> Dict:
        """Main generation pipeline"""
        print("[DISCOVER] Discovering GameAction structs from Go sources...")
        structs = self.discover_go_structs()
        
        if not structs:
            print("[WARN] No GameAction structs found in Go sources")
            return {"error": "No GameAction structs found"}
        
        print(f"[FOUND] Found {len(structs)} GameAction structs:")
        for struct_name, struct_def in structs.items():
            action_code = struct_def['action_code']
            print(f"  - {struct_name} -> Action {action_code}")
        
        print("[GENERATE] Generating Rust subparser files...")
        self.ensure_actions_directory()
        
        for struct_name, struct_def in structs.items():
            if struct_def['action_code'] is not None:
                file_path = self.write_struct_file(struct_name, struct_def)
                print(f"  [OK] Generated {file_path}")
        
        print("[MODULE] Updating actions module...")
        self.update_actions_module(structs)
        
        result = {
            "discovered_structs": len(structs),
            "generated_files": len(self.generated_files),
            "structs": structs,
            "generated_files_list": self.generated_files
        }
        
        print(f"[DONE] Generation complete! Created {len(self.generated_files)} files")
        return result

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate GameAction subparser Rust modules from Go definitions")
    parser.add_argument("--go-source-dir", default="third_party/retroproto/msgsvr",
                       help="Directory containing Go source files")
    parser.add_argument("--rust-output-dir", default="core/src/retroproto_parsers/generated",
                       help="Directory for generated Rust files")
    
    args = parser.parse_args()
    
    generator = GameActionSubparserGenerator(
        go_source_dir=args.go_source_dir,
        rust_output_dir=args.rust_output_dir
    )
    
    result = generator.generate()
    
    # Write generation report
    report_file = Path("core/src/retroproto_parsers/generated/generation_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"[REPORT] Generation report written to {report_file}")
    return 0 if "error" not in result else 1

if __name__ == "__main__":
    sys.exit(main())