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
$RustInput = Join-Path $ExamplesDir "pcap\decoded\dummy_parsed_new.ndjson"
$GoOutputNdjson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.ndjson"
$GoOutputJson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.json"
$DiffJsonOutput = Join-Path $RepoRoot "go_rust_diff.json"
$DiffMdOutput = Join-Path $RepoRoot "GO_RUST_DIFF.md"

# Go binary path
$GoBinary = Join-Path $BinDir "retroproto_go_baseline.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Go Baseline Parser Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check for Go installation
Write-Host "Step 1: Checking Go installation..." -ForegroundColor Yellow
try {
    $goVersion = & go version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Go found: $goVersion" -ForegroundColor Green
    } else {
        throw "Go command failed"
    }
} catch {
    Write-Host "❌ Go not found or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Go:" -ForegroundColor Yellow
    Write-Host "1. Download from https://golang.org/dl/" -ForegroundColor White
    Write-Host "2. Install and add to PATH" -ForegroundColor White
    Write-Host "3. Restart your terminal" -ForegroundColor White
    Write-Host ""
    Write-Host "The Go baseline tools have been created but cannot be run without Go." -ForegroundColor Yellow
    Write-Host "You can run the pipeline manually after installing Go." -ForegroundColor Yellow
    exit 0
}

# Step 2: Ensure bin directory exists
if (-not (Test-Path $BinDir)) {
    Write-Host "Creating bin directory: $BinDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

# Step 3: Generate Go registry
Write-Host ""
Write-Host "Step 2: Generating Go parser registry..." -ForegroundColor Yellow
Push-Location $GoBaselineDir
try {
    & python gen_go_registry.py --out registry.go
    if ($LASTEXITCODE -ne 0) {
        throw "Registry generation failed"
    }
    Write-Host "✅ Registry generated successfully" -ForegroundColor Green
} finally {
    Pop-Location
}

# Step 4: Build Go binary
Write-Host ""
Write-Host "Step 3: Building Go binary..." -ForegroundColor Yellow
Push-Location $GoBaselineDir
try {
    & go build -o $GoBinary
    if ($LASTEXITCODE -ne 0) {
        throw "Go build failed"
    }
    Write-Host "✅ Go binary built successfully: $GoBinary" -ForegroundColor Green
} finally {
    Pop-Location
}

# Check if input file exists
if (-not (Test-Path $RustInput)) {
    Write-Host "❌ Input file not found: $RustInput" -ForegroundColor Red
    Write-Host "Make sure you have run the Rust parser first to generate this file." -ForegroundColor Yellow
    exit 1
}

# Step 5: Run Go parser
Write-Host ""
Write-Host "Step 4: Running Go parser..." -ForegroundColor Yellow
Write-Host "Input: $RustInput" -ForegroundColor Gray
Write-Host "Output NDJSON: $GoOutputNdjson" -ForegroundColor Gray
Write-Host "Output JSON: $GoOutputJson" -ForegroundColor Gray
Write-Host ""

& $GoBinary --in $RustInput --out-ndjson $GoOutputNdjson --out-json $GoOutputJson
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Go parser failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Go parsing completed" -ForegroundColor Green

# Step 6: Run diff tool
Write-Host ""
Write-Host "Step 5: Running diff tool..." -ForegroundColor Yellow
Write-Host "Rust input: $RustInput" -ForegroundColor Gray
Write-Host "Go input: $GoOutputNdjson" -ForegroundColor Gray
Write-Host ""

& python tools\diff_go_rust_parsed.py --rust $RustInput --go $GoOutputNdjson --json-out $DiffJsonOutput --md-out $DiffMdOutput
$diffExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pipeline Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Parse the diff results for summary
if (Test-Path $DiffJsonOutput) {
    try {
        $diffContent = Get-Content $DiffJsonOutput | Out-String | ConvertFrom-Json
        $summary = $diffContent.summary
        
        Write-Host "Total messages processed: $($summary.total)" -ForegroundColor White
        Write-Host "✅ Matches: $($summary.matches) ($([math]::Round($summary.matches/$summary.total*100, 1))%)" -ForegroundColor Green
        Write-Host "❌ Mismatches: $($summary.mismatches) ($([math]::Round($summary.mismatches/$summary.total*100, 1))%)" -ForegroundColor Red
        Write-Host "🔸 Missing in Go: $($summary.missing_go) ($([math]::Round($summary.missing_go/$summary.total*100, 1))%)" -ForegroundColor Yellow
        Write-Host "🔹 Missing in Rust: $($summary.missing_rust) ($([math]::Round($summary.missing_rust/$summary.total*100, 1))%)" -ForegroundColor Magenta
    } catch {
        Write-Host "Could not parse diff summary" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Generated files:" -ForegroundColor White
Write-Host "  📄 Go output (NDJSON): $GoOutputNdjson" -ForegroundColor Gray
Write-Host "  📄 Go output (JSON): $GoOutputJson" -ForegroundColor Gray
Write-Host "  📊 Diff report (JSON): $DiffJsonOutput" -ForegroundColor Gray
Write-Host "  📋 Diff report (Markdown): $DiffMdOutput" -ForegroundColor Gray

if (Test-Path $DiffMdOutput) {
    Write-Host "  📖 Human-readable report: $DiffMdOutput" -ForegroundColor Cyan
}

Write-Host ""
if ($diffExitCode -eq 0) {
    Write-Host "🎉 Perfect match! All parsers agree." -ForegroundColor Green
} else {
    Write-Host "⚠️  Differences found between Rust and Go parsers." -ForegroundColor Yellow
    Write-Host "   See $DiffMdOutput for detailed analysis." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

exit $diffExitCode