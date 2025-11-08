# Parse Integrity Check PowerShell Script
# Runs the NDJSON validator on the Dofus bot parsing output

param(
    [Parameter(Mandatory=$false)]
# DEMO_DISABLED:     [string]$In = "examples\pcap\decoded\dummy_parsed_all.ndjson"
)

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Define paths
$inputPath = $In
$pythonScript = "tools\validate_parsed_integrity.py"
$outputJson = "PARSE_INTEGRITY.json"
$outputMd = "PARSE_INTEGRITY.md"

# Check if input file exists
if (-not (Test-Path $inputPath)) {
    Write-Error "Input file not found: $inputPath"
    exit 1
}

# Check if python script exists
if (-not (Test-Path $pythonScript)) {
    Write-Error "Python script not found: $pythonScript"
    exit 1
}

# Determine Python executable
$pythonExe = $null
if (Test-Path ".venv\Scripts\python.exe") {
    $pythonExe = ".venv\Scripts\python.exe"
# DEMO_DISABLED:     Write-Host "Using virtual environment Python: $pythonExe"
} elseif (Test-Path ".venv\bin\python") {
    $pythonExe = ".venv\bin\python"
# DEMO_DISABLED:     Write-Host "Using virtual environment Python: $pythonExe"
} else {
    # Try system python
    try {
        $pythonExe = & where.exe python
        if ($LASTEXITCODE -eq 0 -and $pythonExe) {
# DEMO_DISABLED:             Write-Host "Using system Python: $pythonExe"
        } else {
            # Try python3
            $pythonExe = & where.exe python3
            if ($LASTEXITCODE -eq 0 -and $pythonExe) {
# DEMO_DISABLED:                 Write-Host "Using system Python3: $pythonExe"
            } else {
                Write-Error "Python not found in PATH"
                exit 1
            }
        }
    } catch {
        Write-Error "Could not find Python executable: $_"
        exit 1
    }
}

# Display what we're about to run
# DEMO_DISABLED: Write-Host "=== Parse Integrity Check ===" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host "Input:    $inputPath"
# DEMO_DISABLED: Write-Host "Script:   $pythonScript"
# DEMO_DISABLED: Write-Host "Output:   $outputJson, $outputMd"
# DEMO_DISABLED: Write-Host "Python:   $pythonExe"
# DEMO_DISABLED: Write-Host "============================" -ForegroundColor Cyan
# DEMO_DISABLED: Write-Host ""

# Run the validator
try {
    & $pythonExe $pythonScript --in $inputPath --out-json $outputJson --out-md $outputMd
    $exitCode = $LASTEXITCODE
    
# DEMO_DISABLED:     Write-Host ""
    if ($exitCode -eq 0) {
# DEMO_DISABLED:         Write-Host "✅ PARSE INTEGRITY CHECK PASSED" -ForegroundColor Green
    } else {
# DEMO_DISABLED:         Write-Host "❌ PARSE INTEGRITY CHECK FAILED (exit code: $exitCode)" -ForegroundColor Red
    }
    
    # Show output file locations
    if (Test-Path $outputJson) {
# DEMO_DISABLED:         Write-Host "📄 JSON report: $outputJson" -ForegroundColor Blue
    }
    if (Test-Path $outputMd) {
# DEMO_DISABLED:         Write-Host "📄 Markdown report: $outputMd" -ForegroundColor Blue
    }
    
    exit $exitCode
} catch {
    Write-Error "Error running validator: $_"
    exit 1
}