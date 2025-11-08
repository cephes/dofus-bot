param(
  [string]$PcapPath = "examples/pcap/john.pcap",
  [switch]$CoreOnly,
  [switch]$SkipRegistry
)

$ErrorActionPreference = "Stop"
function Run($cmd) {
# DEMO_DISABLED:   Write-Host "> $cmd" -ForegroundColor Cyan
  & powershell -NoProfile -Command $cmd
  if ($LASTEXITCODE -ne 0) { throw "Command failed: $cmd" }
}

# 1) regen registry (optional)
if (-not $SkipRegistry) {
  Run "python tools\gen_parser_registry.py"
}

# 2) build dofus-core
$build = "--release -p dofus-core"
if ($CoreOnly) { $build = "--release -p dofus-core" }
Run "cd core; cargo build $build"

# 3) decode PCAP with the debug/rel binary that writes NDJSON
# Expect your existing pipeline to write to examples/pcap/decoded/<name>_parsed_all.ndjson
# If you already have a runner, use it; else call your decoding script/binary.
# We'll use scripts\run_dummy_pipeline.py but with input override and no registry build.
$base = [System.IO.Path]::GetFileNameWithoutExtension($PcapPath)
$decDir = "examples\pcap\decoded"
New-Item -ItemType Directory -Force $decDir | Out-Null
Run "python scripts\run_dummy_pipeline.py --core-only --skip-registry --input `"$PcapPath`" --out-stem `"$base`""

# Expect outputs:
#   $decDir\$base`_parsed_all.ndjson
#   $decDir\$base`_parsed_all.json
$rustNdjson = Join-Path $decDir ($base + "_parsed_all.ndjson")
$rustJson   = Join-Path $decDir ($base + "_parsed_all.json")

if (!(Test-Path $rustNdjson)) { throw "Missing Rust NDJSON: $rustNdjson" }

# 4) run strict Go baseline on *neutral* input
Run "powershell -NoProfile -File scripts\run_go_strict.ps1 -Input `"$rustNdjson`" -OutStem `"$base`""
$goNdjson = Join-Path $decDir ($base + "_go_strict.ndjson")
$goJson   = Join-Path $decDir ($base + "_go_strict.json")
if (!(Test-Path $goNdjson)) { throw "Missing Go NDJSON: $goNdjson" }

# 5) deep diff
Run "python tools\diff_go_rust_parsed.py --rust `"$rustNdjson`" --go `"$goNdjson`" --out-json go_rust_diff.json --out-md GO_RUST_DIFF.md --align-by frame_index,message_name"

# 6) integrity validator
Run "python tools\validate_parsed_integrity.py --in `"$rustNdjson`" --rules tools\validate_rules.yaml --json PARSE_INTEGRITY.json --md PARSE_INTEGRITY.md --fail-on-empty --fail-on-null --fail-on-parse-error"

# 7) tiny console dashboard
$diff = Get-Content go_rust_diff.json | ConvertFrom-Json
$intg = Get-Content PARSE_INTEGRITY.json | ConvertFrom-Json

$matchPercent = [math]::Round(100.0*$diff.matches/[math]::Max(1,$diff.total_rows),1)

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "================= JOHN.PCAP REPORT =================" -ForegroundColor Green
# DEMO_DISABLED: Write-Host "Input frames        : $($diff.total_rows)"
# DEMO_DISABLED: Write-Host "Go-Rust matches     : $($diff.matches)  ($matchPercent%)"
# DEMO_DISABLED: Write-Host "Go-Rust mismatches  : $($diff.mismatches)"
# DEMO_DISABLED: Write-Host "Integrity violations: $($intg.violations_total)"
# DEMO_DISABLED: Write-Host " - empty objects    : $($intg.categories.parsed_empty_object)"
# DEMO_DISABLED: Write-Host " - parse errors     : $($intg.categories.parse_error_present)"
# DEMO_DISABLED: Write-Host " - missing fields   : $($intg.categories.missing_required_field)"
# DEMO_DISABLED: Write-Host " - type mismatch    : $($intg.categories.type_mismatch)"
# DEMO_DISABLED: Write-Host "Artifacts:"
# DEMO_DISABLED: Write-Host " - Rust NDJSON      : $rustNdjson"
# DEMO_DISABLED: Write-Host " - Go   NDJSON      : $goNdjson"
# DEMO_DISABLED: Write-Host " - Diff (json/md)   : go_rust_diff.json / GO_RUST_DIFF.md"
# DEMO_DISABLED: Write-Host " - Integrity (json/md): PARSE_INTEGRITY.json / PARSE_INTEGRITY.md"