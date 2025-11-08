# Repo Diagnostic (2025-11-06 19:33:59)
- Repo root: `d:\WorkDir\dofus-bot`
## Toolchain Versions
- **rustc**: code=0 stdout=`rustc 1.91.0 (f8297e351 2025-10-28)` stderr=``
- **cargo**: code=0 stdout=`cargo 1.91.0 (ea2d97820 2025-10-10)` stderr=``
- **python**: code=0 stdout=`Python 3.14.0` stderr=``
- **go**: code=1 stdout=`` stderr=`'go' is not recognized as an internal or external command,
operable program or batch file.`
- **git**: code=0 stdout=`git version 2.51.2.windows.1` stderr=``

## Key Files Present
- core/Cargo.toml: ✅
- core/src/retroproto_parsers/mod.rs: ✅
- tools/gen_parser_registry.py: ✅
- tools/retroproto_porter_py/porter.py: ✅
- tools/retroproto_porter/main.go: ✅
- third_party/retroproto/mapping_overrides.json: ✅
- third_party/retroproto/mappings_go.txt: ✅
- examples/pcap/dummy.pcap: ❌
- examples/pcap/decoded/dummy_reassembled.json: ✅

## Generated Parsers
- Count .rs: **437**
- First 10: ['core\\src\\retroproto_parsers\\generated\\AccountAddCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAttributeGiftToCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountBoost.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationSuccess.rs']
- Last 10: ['core\\src\\retroproto_parsers\\generated\\SubwayRequestPrismLeave.rs', 'core\\src\\retroproto_parsers\\generated\\SubwayUse.rs', 'core\\src\\retroproto_parsers\\generated\\TutorialCreate.rs', 'core\\src\\retroproto_parsers\\generated\\TutorialEnd.rs', 'core\\src\\retroproto_parsers\\generated\\TutorialGameBegin.rs', 'core\\src\\retroproto_parsers\\generated\\TutorialShowTip.rs', 'core\\src\\retroproto_parsers\\generated\\WaypointsCreate.rs', 'core\\src\\retroproto_parsers\\generated\\WaypointsRequestLeave.rs', 'core\\src\\retroproto_parsers\\generated\\WaypointsUse.rs', 'core\\src\\retroproto_parsers\\generated\\mod.rs']

## Counts
- pub struct: matches=436 (files scanned 437)
- parse_ functions: matches=438 (files scanned 440)
- Registry markers: matches=0

## Cargo Metadata (core/)
- code=0
<details><summary>stdout (truncated)</summary>

```
{"packages":[{"name":"dofus-core","version":"0.1.0","id":"path+file:///D:/WorkDir/dofus-bot/core#dofus-core@0.1.0","license":null,"license_file":null,"description":null,"source":null,"dependencies":[{"name":"anyhow","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^1.0","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":[],"target":null,"registry":null},{"name":"byteorder","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^1.4","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":[],"target":null,"registry":null},{"name":"clap","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^4.0","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":["derive"],"target":null,"registry":null},{"name":"hex","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^0.4","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":[],"target":null,"registry":null},{"name":"once_cell","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^1.19","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":[],"target":null,"registry":null},{"name":"pcap","source":"registry+https://github.com/rust-lang/crates.io-index","req":"^1.1","kind":null,"rename":null,"optional":false,"uses_default_features":true,"features":[],"target":null,"registry":null},{"name":"regex","sour
```
</details>

## Binaries
- reassemble: ✅
  - help.code=0
  <details><summary>stdout</summary>

```
Dofus Retro stream reassembly (whitelist-based)

Usage: reassemble.exe --input <INPUT> --output <OUTPUT>

Options:
      --input <INPUT>    
      --output <OUTPUT>  
  -h, --help             Print help
  -V, --version          Print version
```
</details>
- parse_messages: ✅
  - help.code=101
  <details><summary>stderr</summary>

```
thread 'main' (51172) panicked at src\bin\parse_messages.rs:62:43:
read reassembled json: Os { code: 2, kind: NotFound, message: "The system cannot find the file specified." }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
</details>
- pcap2flow: ✅
  - help.code=3221225781

## Parsed NDJSON Peek
- examples\pcap\decoded\dummy_parsed.ndjson
```
{"frame_index":0,"prefix":"GM","message_name":"GameMovement","parsed":null,"parse_error":"unknown message: Parser for dofus_core::retroproto_parsers::generated::GameMovement not implemented","extra_preview":"GM|~303;5;0;160042728;Blacklist-["}
{"frame_index":1,"prefix":"M","message_name":"AksServerMessage","parsed":null,"parse_error":"unknown message: Parser for dofus_core::retroproto_parsers::generated::AksServerMessage not implemented","extra_preview":"M10];10,85;101^100;1;1,0,1,160042927;ffffff;75293d;cc9b52;2d13,2ce3,2dc1,,;1;;;Irae;8,9lhpx,2w,5rw20;0;60,75293d,cc9b52,"}
{"frame_index":2,"prefix":"GA","message_name":"GameActions","parsed":null,"parse_error":"unknown message: Parser for dofus_core::retroproto_parsers::generated::GameActions not implemented","extra_preview":"GA0;1;121339587;aeVfeGgdjfcRgcofaw"}
{"frame_index":3,"prefix":"GA","message_name":"GameActions","parsed":null,"parse_error":"unknown message: Parser for dofus_core::retroproto_parsers::generated::GameActions not implemented","extra_preview":"GA0;1;121347699;aeVeeUdfkcgedgUchl"}
{"frame_index":4,"prefix":"GM|-","message_name":"GameMovementRemove","parsed":null,"parse_error":"unknown message: Parser for dofus_core::retroproto_parsers::generated::GameMovementRemove not implemented","extra_preview":"GM|-121339587"}
```
- examples\pcap\decoded\dummy_parsed_new.ndjson
```
{"frame_index":0,"prefix":"GM","message_name":"GameMovement","parsed":{"sprites":"~303;5;0;160042728;Blacklist-["},"parse_error":null,"extra_preview":"~303;5;0;160042728;Blacklist-["}
{"frame_index":1,"prefix":"M","message_name":"AksServerMessage","parsed":{"value":"10];10,85;101^100;1;1,0,1,160042927;ffffff;75293d;cc9b52;2d13,2ce3,2dc1,,;1;;;Irae;8,9lhpx,2w,5rw20;0;60,75293d,cc9b52,cc9b52;;0;"},"parse_error":null,"extra_preview":"10];10,85;101^100;1;1,0,1,160042927;ffffff;75293d;cc9b52;2d13,2ce3,2dc1,,;1;;;Irae;8,9lhpx,2w,5rw20;0;60,75293d,cc9b52,c"}
{"frame_index":2,"prefix":"GA","message_name":"GameActions","parsed":{"action_code":0,"rest":"1;121339587;aeVfeGgdjfcRgcofaw"},"parse_error":null,"extra_preview":"0;1;121339587;aeVfeGgdjfcRgcofaw"}
{"frame_index":3,"prefix":"GA","message_name":"GameActions","parsed":{"action_code":0,"rest":"1;121347699;aeVeeUdfkcgedgUchl"},"parse_error":null,"extra_preview":"0;1;121347699;aeVeeUdfkcgedgUchl"}
{"frame_index":4,"prefix":"GM|-","message_name":"GameMovementRemove","parsed":{"id":121339587},"parse_error":null,"extra_preview":"121339587"}
```

## Reassembled JSON
- examples\pcap\decoded\dummy_reassembled.json: len=249, first_entry_keys=['frame_index', 'length', 'message_prefix', 'message_name', 'payload_hex']

## Directory Snapshots (summaries)

### .
- exists: ✅
- dirs: 670 files: 5000 total_bytes: 22731923
- sample files: ['.venv\\.gitignore', '.venv\\Lib\\site-packages\\__pycache__\\typing_extensions.cpython-314.pyc', '.venv\\Lib\\site-packages\\annotated_doc-0.0.3.dist-info\\INSTALLER', '.venv\\Lib\\site-packages\\annotated_doc-0.0.3.dist-info\\METADATA', '.venv\\Lib\\site-packages\\annotated_doc-0.0.3.dist-info\\RECORD', '.venv\\Lib\\site-packages\\annotated_doc-0.0.3.dist-info\\WHEEL', '.venv\\Lib\\site-packages\\annotated_doc-0.0.3.dist-info\\licenses\\LICENSE', '.venv\\Lib\\site-packages\\annotated_doc\\__init__.py', '.venv\\Lib\\site-packages\\annotated_doc\\__pycache__\\__init__.cpython-314.pyc', '.venv\\Lib\\site-packages\\annotated_doc\\__pycache__\\main.cpython-314.pyc', '.venv\\Lib\\site-packages\\annotated_doc\\main.py', '.venv\\Lib\\site-packages\\annotated_doc\\py.typed', '.venv\\Lib\\site-packages\\annotated_types-0.7.0.dist-info\\INSTALLER', '.venv\\Lib\\site-packages\\annotated_types-0.7.0.dist-info\\METADATA', '.venv\\Lib\\site-packages\\annotated_types-0.7.0.dist-info\\RECORD', '.venv\\Lib\\site-packages\\annotated_types-0.7.0.dist-info\\WHEEL', '.venv\\Lib\\site-packages\\annotated_types-0.7.0.dist-info\\licenses\\LICENSE', '.venv\\Lib\\site-packages\\annotated_types\\__init__.py', '.venv\\Lib\\site-packages\\annotated_types\\__pycache__\\__init__.cpython-314.pyc', '.venv\\Lib\\site-packages\\annotated_types\\__pycache__\\test_cases.cpython-314.pyc']

### core
- exists: ✅
- dirs: 277 files: 2184 total_bytes: 27757214
- sample files: ['core\\Cargo.lock', 'core\\Cargo.toml', 'core\\README.md', 'core\\comprehensive_fix.py', 'core\\dummy.pcap', 'core\\fix_all', 'core\\fix_all_remaining', 'core\\fix_all_syntax.py', 'core\\fix_double_braces.py', 'core\\fix_double_braces_simple.py', 'core\\fix_double_delimiters.py', 'core\\fix_extra_parentheses.py', 'core\\fix_missing_braces.py', 'core\\fix_missing_parentheses_semicol', 'core\\fix_missing_parentheses_semicolons.py', 'core\\fix_missing_semicolons.py', 'core\\fix_ok_expressions.py', 'core\\fix_ok_expressions_precise.py', 'core\\fix_ok_expressions_v2.py', 'core\\fix_specific_double_braces.py']

### core/src
- exists: ✅
- dirs: 7 files: 478 total_bytes: 370201
- sample files: ['core\\src\\bin\\parse_messages.rs', 'core\\src\\bin\\pcap2flow.rs', 'core\\src\\bin\\reassemble.rs', 'core\\src\\dofus_framing.rs', 'core\\src\\dofus_mapping.rs', 'core\\src\\dofus_mapping_ext.rs', 'core\\src\\dofus_mapping_types.rs', 'core\\src\\dofus_proto.rs', 'core\\src\\lib.rs', 'core\\src\\main.rs', 'core\\src\\parser\\mod.rs', 'core\\src\\parser\\prefix_scan.rs', 'core\\src\\parser\\reassembly.rs', 'core\\src\\parser\\splitter.rs', 'core\\src\\retroproto', 'core\\src\\retroproto_', 'core\\src\\retroproto_parsers\\generated\\Account', 'core\\src\\retroproto_parsers\\generated\\AccountAddCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacter', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration']

### core/src/bin
- exists: ✅
- dirs: 1 files: 3 total_bytes: 24074
- sample files: ['core\\src\\bin\\parse_messages.rs', 'core\\src\\bin\\pcap2flow.rs', 'core\\src\\bin\\reassemble.rs', 'core\\src\\bin\\parse_messages.rs', 'core\\src\\bin\\pcap2flow.rs', 'core\\src\\bin\\reassemble.rs']

### core/src/retroproto_parsers
- exists: ✅
- dirs: 4 files: 462 total_bytes: 300540
- sample files: ['core\\src\\retroproto_parsers\\generated\\Account', 'core\\src\\retroproto_parsers\\generated\\AccountAddCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacter', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAttributeGiftToCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountBoost.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterNameGeneratedError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterNameGeneratedSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterSelectedError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterSelectedSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharactersListError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharactersListSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCommunity.rs']

### core/src/retroproto_parsers/generated
- exists: ✅
- dirs: 2 files: 457 total_bytes: 115727
- sample files: ['core\\src\\retroproto_parsers\\generated\\Account', 'core\\src\\retroproto_parsers\\generated\\AccountAddCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacter', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration', 'core\\src\\retroproto_parsers\\generated\\AccountAskCharacterMigration.rs', 'core\\src\\retroproto_parsers\\generated\\AccountAttributeGiftToCharacter.rs', 'core\\src\\retroproto_parsers\\generated\\AccountBoost.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterAddSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterDeleteSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterMigrationSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterNameGeneratedError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterNameGeneratedSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterSelectedError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharacterSelectedSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharactersListError.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCharactersListSuccess.rs', 'core\\src\\retroproto_parsers\\generated\\AccountCommunity.rs']

### core/src/retroproto_parsers/handwritten
- exists: ✅
- dirs: 1 files: 3 total_bytes: 8310
- sample files: ['core\\src\\retroproto_parsers\\handwritten\\GameActions.rs', 'core\\src\\retroproto_parsers\\handwritten\\GameEffect.rs', 'core\\src\\retroproto_parsers\\handwritten\\mod.rs', 'core\\src\\retroproto_parsers\\handwritten\\GameActions.rs', 'core\\src\\retroproto_parsers\\handwritten\\GameEffect.rs', 'core\\src\\retroproto_parsers\\handwritten\\mod.rs']

### core/target/release
- exists: ✅
- dirs: 121 files: 612 total_bytes: 27673013
- sample files: ['core\\target\\release\\.cargo-lock', 'core\\target\\release\\.fingerprint\\aho-corasick-44fd382148fbe705\\dep-lib-aho_corasick', 'core\\target\\release\\.fingerprint\\aho-corasick-44fd382148fbe705\\invoked.timestamp', 'core\\target\\release\\.fingerprint\\aho-corasick-44fd382148fbe705\\lib-aho_corasick', 'core\\target\\release\\.fingerprint\\aho-corasick-44fd382148fbe705\\lib-aho_corasick.json', 'core\\target\\release\\.fingerprint\\aho-corasick-c0bab61e37b16cbd\\dep-lib-aho_corasick', 'core\\target\\release\\.fingerprint\\aho-corasick-c0bab61e37b16cbd\\invoked.timestamp', 'core\\target\\release\\.fingerprint\\aho-corasick-c0bab61e37b16cbd\\lib-aho_corasick', 'core\\target\\release\\.fingerprint\\aho-corasick-c0bab61e37b16cbd\\lib-aho_corasick.json', 'core\\target\\release\\.fingerprint\\anstream-c6ded74c523b28b9\\dep-lib-anstream', 'core\\target\\release\\.fingerprint\\anstream-c6ded74c523b28b9\\invoked.timestamp', 'core\\target\\release\\.fingerprint\\anstream-c6ded74c523b28b9\\lib-anstream', 'core\\target\\release\\.fingerprint\\anstream-c6ded74c523b28b9\\lib-anstream.json', 'core\\target\\release\\.fingerprint\\anstyle-6357e80b4866bb61\\dep-lib-anstyle', 'core\\target\\release\\.fingerprint\\anstyle-6357e80b4866bb61\\invoked.timestamp', 'core\\target\\release\\.fingerprint\\anstyle-6357e80b4866bb61\\lib-anstyle', 'core\\target\\release\\.fingerprint\\anstyle-6357e80b4866bb61\\lib-anstyle.json', 'core\\target\\release\\.fingerprint\\anstyle-parse-537db6ff7148dfb9\\dep-lib-anstyle_parse', 'core\\target\\release\\.fingerprint\\anstyle-parse-537db6ff7148dfb9\\invoked.timestamp', 'core\\target\\release\\.fingerprint\\anstyle-parse-537db6ff7148dfb9\\lib-anstyle_parse']

### tools
- exists: ✅
- dirs: 3 files: 13 total_bytes: 151820
- sample files: ['tools\\find_plaintext_flow.py', 'tools\\gen_parser_registry.py', 'tools\\generate_prefix_counts.py', 'tools\\infer_retroproto_mapping.py', 'tools\\list_structs.py', 'tools\\regen_and_parse.py', 'tools\\retroproto_porter\\main.go', 'tools\\retroproto_porter\\run_porter.sh', 'tools\\retroproto_porter_py\\porter.py', 'tools\\retroproto_porter_py\\porter.py.bak', 'tools\\retroproto_porter_py\\porter.py.pre_regex_fix.bak', 'tools\\retroproto_porter_py\\run_porter.ps1', 'tools\\silence_snake_warnings.py', 'tools\\find_plaintext_flow.py', 'tools\\gen_parser_registry.py', 'tools\\generate_prefix_counts.py', 'tools\\infer_retroproto_mapping.py', 'tools\\list_structs.py', 'tools\\regen_and_parse.py', 'tools\\retroproto_porter\\main.go']

### tools/retroproto_porter_py
- exists: ✅
- dirs: 1 files: 4 total_bytes: 92626
- sample files: ['tools\\retroproto_porter_py\\porter.py', 'tools\\retroproto_porter_py\\porter.py.bak', 'tools\\retroproto_porter_py\\porter.py.pre_regex_fix.bak', 'tools\\retroproto_porter_py\\run_porter.ps1', 'tools\\retroproto_porter_py\\porter.py', 'tools\\retroproto_porter_py\\porter.py.bak', 'tools\\retroproto_porter_py\\porter.py.pre_regex_fix.bak', 'tools\\retroproto_porter_py\\run_porter.ps1']

### tools/retroproto_porter
- exists: ✅
- dirs: 1 files: 2 total_bytes: 21590
- sample files: ['tools\\retroproto_porter\\main.go', 'tools\\retroproto_porter\\run_porter.sh', 'tools\\retroproto_porter\\main.go', 'tools\\retroproto_porter\\run_porter.sh']

### scripts
- exists: ✅
- dirs: 1 files: 3 total_bytes: 27048
- sample files: ['scripts\\diagnose_repo.py', 'scripts\\run_dummy_parsing.ps1', 'scripts\\run_dummy_pipeline.py', 'scripts\\diagnose_repo.py', 'scripts\\run_dummy_parsing.ps1', 'scripts\\run_dummy_pipeline.py']

### examples
- exists: ✅
- dirs: 4 files: 22 total_bytes: 1838113
- sample files: ['examples\\pcap\\decoded\\_plaintext_flow_probe.json', 'examples\\pcap\\decoded\\decoder_run_stderr.log', 'examples\\pcap\\decoded\\decoder_run_stdout.log', 'examples\\pcap\\decoded\\dummy_parsed.json', 'examples\\pcap\\decoded\\dummy_parsed.ndjson', 'examples\\pcap\\decoded\\dummy_parsed_new.json', 'examples\\pcap\\decoded\\dummy_parsed_new.ndjson', 'examples\\pcap\\decoded\\dummy_reassembled.json', 'examples\\pcap\\decoded\\flow_dummy_decoded.json', 'examples\\pcap\\decoded\\flow_dummy_parsed_summary.json', 'examples\\pcap\\decoded\\flow_ported_parsed.json', 'examples\\pcap\\decoded\\flow_reassembled.ndjson', 'examples\\pcap\\decoded\\flow_reassembled_decoded.json', 'examples\\pcap\\decoded\\flow_reassembled_named_summary.json', 'examples\\pcap\\decoded\\flow_reassembled_with_names.json', 'examples\\pcap\\decoded\\none_continuation_analysis.json', 'examples\\pcap\\decoded\\none_continuation_examples.json', 'examples\\pcap\\decoded\\reassemble_quick_summary.json', 'examples\\pcap\\decoded\\reassemble_run_stderr.log', 'examples\\pcap\\decoded\\reassemble_run_stdout.log']

### examples/pcap
- exists: ✅
- dirs: 3 files: 22 total_bytes: 1838113
- sample files: ['examples\\pcap\\decoded\\_plaintext_flow_probe.json', 'examples\\pcap\\decoded\\decoder_run_stderr.log', 'examples\\pcap\\decoded\\decoder_run_stdout.log', 'examples\\pcap\\decoded\\dummy_parsed.json', 'examples\\pcap\\decoded\\dummy_parsed.ndjson', 'examples\\pcap\\decoded\\dummy_parsed_new.json', 'examples\\pcap\\decoded\\dummy_parsed_new.ndjson', 'examples\\pcap\\decoded\\dummy_reassembled.json', 'examples\\pcap\\decoded\\flow_dummy_decoded.json', 'examples\\pcap\\decoded\\flow_dummy_parsed_summary.json', 'examples\\pcap\\decoded\\flow_ported_parsed.json', 'examples\\pcap\\decoded\\flow_reassembled.ndjson', 'examples\\pcap\\decoded\\flow_reassembled_decoded.json', 'examples\\pcap\\decoded\\flow_reassembled_named_summary.json', 'examples\\pcap\\decoded\\flow_reassembled_with_names.json', 'examples\\pcap\\decoded\\none_continuation_analysis.json', 'examples\\pcap\\decoded\\none_continuation_examples.json', 'examples\\pcap\\decoded\\reassemble_quick_summary.json', 'examples\\pcap\\decoded\\reassemble_run_stderr.log', 'examples\\pcap\\decoded\\reassemble_run_stdout.log']

### examples/pcap/flows
- exists: ✅
- dirs: 1 files: 1 total_bytes: 57122
- sample files: ['examples\\pcap\\flows\\flow_000_TCP_192.168.1.8_2485_52.214.173.25_443.bin', 'examples\\pcap\\flows\\flow_000_TCP_192.168.1.8_2485_52.214.173.25_443.bin']

### examples/pcap/decoded
- exists: ✅
- dirs: 1 files: 21 total_bytes: 1809552
- sample files: ['examples\\pcap\\decoded\\_plaintext_flow_probe.json', 'examples\\pcap\\decoded\\decoder_run_stderr.log', 'examples\\pcap\\decoded\\decoder_run_stdout.log', 'examples\\pcap\\decoded\\dummy_parsed.json', 'examples\\pcap\\decoded\\dummy_parsed.ndjson', 'examples\\pcap\\decoded\\dummy_parsed_new.json', 'examples\\pcap\\decoded\\dummy_parsed_new.ndjson', 'examples\\pcap\\decoded\\dummy_reassembled.json', 'examples\\pcap\\decoded\\flow_dummy_decoded.json', 'examples\\pcap\\decoded\\flow_dummy_parsed_summary.json', 'examples\\pcap\\decoded\\flow_ported_parsed.json', 'examples\\pcap\\decoded\\flow_reassembled.ndjson', 'examples\\pcap\\decoded\\flow_reassembled_decoded.json', 'examples\\pcap\\decoded\\flow_reassembled_named_summary.json', 'examples\\pcap\\decoded\\flow_reassembled_with_names.json', 'examples\\pcap\\decoded\\none_continuation_analysis.json', 'examples\\pcap\\decoded\\none_continuation_examples.json', 'examples\\pcap\\decoded\\reassemble_quick_summary.json', 'examples\\pcap\\decoded\\reassemble_run_stderr.log', 'examples\\pcap\\decoded\\reassemble_run_stdout.log']

### third_party
- exists: ✅
- dirs: 10 files: 553 total_bytes: 67713
- sample files: ['third_party\\retroproto\\.gitignore', 'third_party\\retroproto\\LICENSE', 'third_party\\retroproto\\MAPPING_REPORT.md', 'third_party\\retroproto\\README.md', 'third_party\\retroproto\\assets\\conn.puml', 'third_party\\retroproto\\assets\\template.msgcli.txt', 'third_party\\retroproto\\assets\\template.msgsvr.txt', 'third_party\\retroproto\\cmd\\delgen\\main.go', 'third_party\\retroproto\\cmd\\genmsgs\\main.go', 'third_party\\retroproto\\crypto.go', 'third_party\\retroproto\\enum\\accountcharacteradderrorreason.go', 'third_party\\retroproto\\enum\\accountcharacternamegeneratederrorreason.go', 'third_party\\retroproto\\enum\\accountloginerrorreason.go', 'third_party\\retroproto\\enum\\accountselectservererrorreason.go', 'third_party\\retroproto\\enum\\basicssubscriberrestrictionadddialogid.go', 'third_party\\retroproto\\enum\\chatmessageerrorreason.go', 'third_party\\retroproto\\enum\\exchangerequesterrorreason.go', 'third_party\\retroproto\\enum\\gameactionchallengejoinerrorreason.go', 'third_party\\retroproto\\enum\\gameactiontype.go', 'third_party\\retroproto\\enum\\gamecreatetype.go']

### third_party/retroproto
- exists: ✅
- dirs: 9 files: 553 total_bytes: 67713
- sample files: ['third_party\\retroproto\\.gitignore', 'third_party\\retroproto\\LICENSE', 'third_party\\retroproto\\MAPPING_REPORT.md', 'third_party\\retroproto\\README.md', 'third_party\\retroproto\\assets\\conn.puml', 'third_party\\retroproto\\assets\\template.msgcli.txt', 'third_party\\retroproto\\assets\\template.msgsvr.txt', 'third_party\\retroproto\\cmd\\delgen\\main.go', 'third_party\\retroproto\\cmd\\genmsgs\\main.go', 'third_party\\retroproto\\crypto.go', 'third_party\\retroproto\\enum\\accountcharacteradderrorreason.go', 'third_party\\retroproto\\enum\\accountcharacternamegeneratederrorreason.go', 'third_party\\retroproto\\enum\\accountloginerrorreason.go', 'third_party\\retroproto\\enum\\accountselectservererrorreason.go', 'third_party\\retroproto\\enum\\basicssubscriberrestrictionadddialogid.go', 'third_party\\retroproto\\enum\\chatmessageerrorreason.go', 'third_party\\retroproto\\enum\\exchangerequesterrorreason.go', 'third_party\\retroproto\\enum\\gameactionchallengejoinerrorreason.go', 'third_party\\retroproto\\enum\\gameactiontype.go', 'third_party\\retroproto\\enum\\gamecreatetype.go']

### third_party/retroproto/msgsvr
- exists: ✅
- dirs: 1 files: 309 total_bytes: 38719
- sample files: ['third_party\\retroproto\\msgsvr\\accountcharacteradderror.go', 'third_party\\retroproto\\msgsvr\\accountcharacteraddsuccess.go', 'third_party\\retroproto\\msgsvr\\accountcharacterdeleteerror.go', 'third_party\\retroproto\\msgsvr\\accountcharacterdeletesuccess.go', 'third_party\\retroproto\\msgsvr\\accountcharactermigrationaskconfirm.go', 'third_party\\retroproto\\msgsvr\\accountcharactermigrationerror.go', 'third_party\\retroproto\\msgsvr\\accountcharactermigrationsuccess.go', 'third_party\\retroproto\\msgsvr\\accountcharacternamegeneratederror.go', 'third_party\\retroproto\\msgsvr\\accountcharacternamegeneratedsuccess.go', 'third_party\\retroproto\\msgsvr\\accountcharacterselectederror.go', 'third_party\\retroproto\\msgsvr\\accountcharacterselectedsuccess.go', 'third_party\\retroproto\\msgsvr\\accountcharacterslisterror.go', 'third_party\\retroproto\\msgsvr\\accountcharacterslistsuccess.go', 'third_party\\retroproto\\msgsvr\\accountcommunity.go', 'third_party\\retroproto\\msgsvr\\accountfriendserverlist.go', 'third_party\\retroproto\\msgsvr\\accountgiftslist.go', 'third_party\\retroproto\\msgsvr\\accountgiftstorederror.go', 'third_party\\retroproto\\msgsvr\\accountgiftstoredsuccess.go', 'third_party\\retroproto\\msgsvr\\accounthosts.go', 'third_party\\retroproto\\msgsvr\\accountkey.go']

### third_party/retroproto/msgcli
- exists: ✅
- dirs: 1 files: 195 total_bytes: 35330
- sample files: ['third_party\\retroproto\\msgcli\\accountaddcharacter.go', 'third_party\\retroproto\\msgcli\\accountaskcharactermigration.go', 'third_party\\retroproto\\msgcli\\accountattributegifttocharacter.go', 'third_party\\retroproto\\msgcli\\accountboost.go', 'third_party\\retroproto\\msgcli\\accountconfiguredport.go', 'third_party\\retroproto\\msgcli\\accountcredential.go', 'third_party\\retroproto\\msgcli\\accountdeletecharacter.go', 'third_party\\retroproto\\msgcli\\accountdeletecharactermigration.go', 'third_party\\retroproto\\msgcli\\accountgetcharacters.go', 'third_party\\retroproto\\msgcli\\accountgetcharactersforced.go', 'third_party\\retroproto\\msgcli\\accountgetgifts.go', 'third_party\\retroproto\\msgcli\\accountgetrandomcharactername.go', 'third_party\\retroproto\\msgcli\\accountgetserverslist.go', 'third_party\\retroproto\\msgcli\\accountqueueposition.go', 'third_party\\retroproto\\msgcli\\accountrequestregionalversion.go', 'third_party\\retroproto\\msgcli\\accountrequestrescue.go', 'third_party\\retroproto\\msgcli\\accountresetcharacter.go', 'third_party\\retroproto\\msgcli\\accountsearchforfriend.go', 'third_party\\retroproto\\msgcli\\accountsendidentity.go', 'third_party\\retroproto\\msgcli\\accountsendticket.go']