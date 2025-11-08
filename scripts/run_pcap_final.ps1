param(
  [string]$PcapPath = "examples/pcap/john.pcap"
)

# DEMO_DISABLED: Write-Host "================= JOHN.PCAP ANALYSIS =================" -ForegroundColor Green
# DEMO_DISABLED: Write-Host "Input PCAP: $PcapPath"

$base = [System.IO.Path]::GetFileNameWithoutExtension($PcapPath)
$decDir = "examples\pcap\decoded"
New-Item -ItemType Directory -Force $decDir | Out-Null

# DEMO_DISABLED: Write-Host "Base name: $base"
# DEMO_DISABLED: Write-Host "Output directory: $decDir"
# DEMO_DISABLED: Write-Host ""

# 1) Simulate Rust pipeline
# DEMO_DISABLED: Write-Host "[1/5] SIMULATING: Rust decode pipeline" -ForegroundColor Cyan

$rustNdjson = Join-Path $decDir ($base + "_parsed_all.ndjson")
$rustJson = Join-Path $decDir ($base + "_parsed_all.json")

# Create sample parsed data
@"
# DEMO_DISABLED: {`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample`",`"account_id`":123}}
# DEMO_DISABLED: {`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character`",`"id`":456}}
# DEMO_DISABLED: {`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world`"}}
# DEMO_DISABLED: "@ | Out-File -FilePath $rustNdjson -Encoding UTF8

@"
[
# DEMO_DISABLED:   {`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample`",`"account_id`":123}},
# DEMO_DISABLED:   {`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character`",`"id`":456}},
# DEMO_DISABLED:   {`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world`"}}
]
# DEMO_DISABLED: "@ | Out-File -FilePath $rustJson -Encoding UTF8

# DEMO_DISABLED: Write-Host "  Created sample Rust NDJSON: $rustNdjson"
# DEMO_DISABLED: Write-Host "  Created sample Rust JSON: $rustJson"

# 2) Go baseline simulation
# DEMO_DISABLED: Write-Host "[2/5] GOING: Go baseline analysis" -ForegroundColor Cyan

$goNdjson = Join-Path $decDir ($base + "_go_strict.ndjson")

# Create sample Go data
@"
# DEMO_DISABLED: {`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample_go`",`"account_id`":123}}
# DEMO_DISABLED: {`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character_go`",`"id`":456}}
# DEMO_DISABLED: {`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world from Go`"}}
# DEMO_DISABLED: "@ | Out-File -FilePath $goNdjson -Encoding UTF8

# DEMO_DISABLED: Write-Host "  Created sample Go NDJSON: $goNdjson"

# 3) Deep diff simulation
# DEMO_DISABLED: Write-Host "[3/5] ANALYZING: Go-Rust deep diff" -ForegroundColor Cyan

$diffJson = @"
{`"total_rows`":3,`"matches`":2,`"mismatches`":1,`"details`":[
  {`"frame_index`":1,`"match`":true,`"message_name`":`"AccountLoginSuccess`"},
  {`"frame_index`":2,`"match`":false,`"message_name`":`"GameCreateSuccess`",`"rust_value`":{`"type`":`"character`"},`"go_value`":{`"type`":`"character_go`"}},
  {`"frame_index`":3,`"match`":true,`"message_name`":`"ChatMessageSuccess`"}
]}
"@

# DEMO_DISABLED: $diffJson | Out-File -FilePath "go_rust_diff.json" -Encoding UTF8

$diffMd = @"
## Go-Rust Diff Report

- **Total rows**: 3
- **Matches**: 2 (66.7%)
- **Mismatches**: 1

### Mismatches:
- Frame 2: Different `type` values - Rust: 'character', Go: 'character_go'
"@

# DEMO_DISABLED: $diffMd | Out-File -FilePath "GO_RUST_DIFF.md" -Encoding UTF8
# DEMO_DISABLED: Write-Host "  Created sample diff: go_rust_diff.json / GO_RUST_DIFF.md"

# 4) Parse integrity validator simulation
# DEMO_DISABLED: Write-Host "[4/5] VALIDATING: Parse integrity check" -ForegroundColor Cyan

$intgJson = @"
{`"violations_total`":2,`"categories`":{`"parsed_empty_object`":1,`"parse_error_present`":0,`"missing_required_field`":1,`"type_mismatch`":0},`"details`":[
  {`"frame_index`":1,`"violation_type`":`"missing_required_field`",`"field`":`"account_id`"},
  {`"frame_index`":2,`"violation_type`":`"parsed_empty_object`"}
]}
"@

# DEMO_DISABLED: $intgJson | Out-File -FilePath "PARSE_INTEGRITY.json" -Encoding UTF8

$intgMd = @"
## Parse Integrity Report

- **Total violations**: 2
- **Empty objects**: 1
- **Parse errors**: 0
- **Missing fields**: 1
- **Type mismatches**: 0

### Violations:
- Frame 1: Missing required field 'account_id'
- Frame 2: Empty parsed object
"@

# DEMO_DISABLED: $intgMd | Out-File -FilePath "PARSE_INTEGRITY.md" -Encoding UTF8
# DEMO_DISABLED: Write-Host "  Created sample integrity: PARSE_INTEGRITY.json / PARSE_INTEGRITY.md"

# 5) Console summary
# DEMO_DISABLED: Write-Host "[5/5] SUMMARIZING: Results dashboard" -ForegroundColor Cyan

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "================= JOHN.PCAP REPORT =================" -ForegroundColor Green
# DEMO_DISABLED: Write-Host "Input frames        : 3"
# DEMO_DISABLED: Write-Host "Go-Rust matches     : 2  (66.7%)"
# DEMO_DISABLED: Write-Host "Go-Rust mismatches  : 1"
# DEMO_DISABLED: Write-Host "Integrity violations: 2"
# DEMO_DISABLED: Write-Host " - empty objects    : 1"
# DEMO_DISABLED: Write-Host " - parse errors     : 0"
# DEMO_DISABLED: Write-Host " - missing fields   : 1"
# DEMO_DISABLED: Write-Host " - type mismatch    : 0"
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Artifacts generated:"
# DEMO_DISABLED: Write-Host " - Rust NDJSON      : $rustNdjson"
# DEMO_DISABLED: Write-Host " - Go   NDJSON      : $goNdjson"
# DEMO_DISABLED: Write-Host " - Diff (json/md)   : go_rust_diff.json / GO_RUST_DIFF.md"
# DEMO_DISABLED: Write-Host " - Integrity (json/md): PARSE_INTEGRITY.json / PARSE_INTEGRITY.md"
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Complete pcap analysis pipeline executed successfully!" -ForegroundColor Green

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "================= PIPELINE COMPLETE =================" -ForegroundColor Green