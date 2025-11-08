#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run the Go baseline parser and diff tool pipeline

.DESCRIPTION
    This script orchestrates the complete Go baseline pipeline:
    1. Checks for Go installation
    2. Generates the Go parser registry
    3. Builds the Go binary
    4. Runs the Go parser on sample data
    5. Compares Go vs Rust outputs
    6. Generates reports
#>

$ErrorActionPreference = "Stop"

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

# Output directories
$BinDir = Join-Path $RepoRoot "bin"
$ExamplesDir = Join-Path $RepoRoot "examples"
$GoBaselineDir = Join-Path $RepoRoot "tools\go_baseline"

# Input files
# DEMO_DISABLED: $RustInput = Join-Path $ExamplesDir "pcap\decoded\dummy_parsed_new.ndjson"
# DEMO_DISABLED: $GoOutputNdjson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.ndjson"
# DEMO_DISABLED: $GoOutputJson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.json"
$DiffJsonOutput = Join-Path $RepoRoot "go_rust_diff.json"
$DiffMdOutput = Join-Path $RepoRoot "GO_RUST_DIFF.md"

# Go binary path
$GoBinary = Join-Path $BinDir "retroproto_go_baseline.exe"

# DEMO_DISABLED: Write-Host "========================================" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host "Go Baseline Parser Pipeline" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host "========================================" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host ""

# Step 1: Check for Go installation
# DEMO_DISABLED: Write-Host "Step 1: Checking Go installation..." -ForegroundColor Yellow
try {
    $goVersion = & go version 2>$null
    if ($LASTEXITCODE -eq 0) {
# DEMO_DISABLED:         Write-Host "✅ Go found: $goVersion" -ForegroundColor Green
    } else {
        throw "Go command failed"
    }
} catch {
# DEMO_DISABLED:     Write-Host "❌ Go not found or not in PATH" -ForegroundColor Red
# DEMO_DISABLED:     Write-Host ""
# DEMO_DISABLED:     Write-Host "To install Go:" -ForegroundColor Yellow
# DEMO_DISABLED:     Write-Host "1. Download from https://golang.org/dl/" -ForegroundColor White
# DEMO_DISABLED:     Write-Host "2. Install and add to PATH" -ForegroundColor White
# DEMO_DISABLED:     Write-Host "3. Restart your terminal" -ForegroundColor White
# DEMO_DISABLED:     Write-Host ""
# DEMO_DISABLED:     Write-Host "The Go baseline tools have been created but cannot be run without Go." -ForegroundColor Yellow
# DEMO_DISABLED:     Write-Host "You can run the pipeline manually after installing Go." -ForegroundColor Yellow
    exit 0
}

# Step 2: Ensure bin directory exists
if (-not (Test-Path $BinDir)) {
# DEMO_DISABLED:     Write-Host "Creating bin directory: $BinDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

# Step 3: Generate Go registry
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Step 2: Generating Go parser registry..." -ForegroundColor Yellow
Push-Location $GoBaselineDir
try {
    & python gen_go_registry.py --out registry.go
    if ($LASTEXITCODE -ne 0) {
        throw "Registry generation failed"
    }
# DEMO_DISABLED:     Write-Host "✅ Registry generated successfully" -ForegroundColor Green
} finally {
    Pop-Location
}

# Step 4: Build Go binary
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Step 3: Building Go binary..." -ForegroundColor Yellow
Push-Location $GoBaselineDir
try {
    & go build -o $GoBinary
    if ($LASTEXITCODE -ne 0) {
        throw "Go build failed"
    }
# DEMO_DISABLED:     Write-Host "✅ Go binary built successfully: $GoBinary" -ForegroundColor Green
} finally {
    Pop-Location
}

# Check if input file exists
if (-not (Test-Path $RustInput)) {
# DEMO_DISABLED:     Write-Host "❌ Input file not found: $RustInput" -ForegroundColor Red
# DEMO_DISABLED:     Write-Host "Make sure you have run the Rust parser first to generate this file." -ForegroundColor Yellow
    exit 1
}

# Step 5: Run Go parser
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Step 4: Running Go parser..." -ForegroundColor Yellow
# DEMO_DISABLED: Write-Host "Input: $RustInput" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "Output NDJSON: $GoOutputNdjson" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "Output JSON: $GoOutputJson" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host ""

& $GoBinary --in $RustInput --out-ndjson $GoOutputNdjson --out-json $GoOutputJson
if ($LASTEXITCODE -ne 0) {
# DEMO_DISABLED:     Write-Host "❌ Go parser failed" -ForegroundColor Red
    exit 1
}
# DEMO_DISABLED: Write-Host "✅ Go parsing completed" -ForegroundColor Green

# Step 6: Run diff tool
# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Step 5: Running diff tool..." -ForegroundColor Yellow
# DEMO_DISABLED: Write-Host "Rust input: $RustInput" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "Go input: $GoOutputNdjson" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host ""

& python tools\diff_go_rust_parsed.py --rust $RustInput --go $GoOutputNdjson --json-out $DiffJsonOutput --md-out $DiffMdOutput
$diffExitCode = $LASTEXITCODE

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "========================================" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host "Pipeline Summary" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host "========================================" -ForegroundColor Cyan

# Parse the diff results for summary
if (Test-Path $DiffJsonOutput) {
    try {
        $diffContent = Get-Content $DiffJsonOutput | Out-String | ConvertFrom-Json
        $summary = $diffContent.summary
        
# DEMO_DISABLED:         Write-Host "Total messages processed: $($summary.total)" -ForegroundColor White
# DEMO_DISABLED:         Write-Host "✅ Matches: $($summary.matches) ($([math]::Round($summary.matches/$summary.total*100, 1))%)" -ForegroundColor Green
# DEMO_DISABLED:         Write-Host "❌ Mismatches: $($summary.mismatches) ($([math]::Round($summary.mismatches/$summary.total*100, 1))%)" -ForegroundColor Red
# DEMO_DISABLED:         Write-Host "🔸 Missing in Go: $($summary.missing_go) ($([math]::Round($summary.missing_go/$summary.total*100, 1))%)" -ForegroundColor Yellow
# DEMO_DISABLED:         Write-Host "🔹 Missing in Rust: $($summary.missing_rust) ($([math]::Round($summary.missing_rust/$summary.total*100, 1))%)" -ForegroundColor Magenta
    } catch {
# DEMO_DISABLED:         Write-Host "Could not parse diff summary" -ForegroundColor Yellow
    }
}

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "Generated files:" -ForegroundColor White
# DEMO_DISABLED: Write-Host "  📄 Go output (NDJSON): $GoOutputNdjson" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "  📄 Go output (JSON): $GoOutputJson" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "  📊 Diff report (JSON): $DiffJsonOutput" -ForegroundColor Gray
# DEMO_DISABLED: Write-Host "  📋 Diff report (Markdown): $DiffMdOutput" -ForegroundColor Gray

if (Test-Path $DiffMdOutput) {
# DEMO_DISABLED:     Write-Host "  📖 Human-readable report: $DiffMdOutput" -ForegroundColor Cyan
}

# DEMO_DISABLED: Write-Host ""
if ($diffExitCode -eq 0) {
# DEMO_DISABLED:     Write-Host "🎉 Perfect match! All parsers agree." -ForegroundColor Green
} else {
# DEMO_DISABLED:     Write-Host "⚠️  Differences found between Rust and Go parsers." -ForegroundColor Yellow
# DEMO_DISABLED:     Write-Host "   See $DiffMdOutput for detailed analysis." -ForegroundColor Yellow
}

# DEMO_DISABLED: Write-Host ""
# DEMO_DISABLED: Write-Host "========================================" -ForegroundColor Cyan

exit $diffExitCode