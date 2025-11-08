$ErrorActionPreference = "Stop"

function Write-Section($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }

# 0) Guard: prevent accidental parser regeneration during recovery
$regenFlag = "tools\GEN_REGEN_DISABLED.flag"
New-Item -ItemType Directory -Force -Path "tools" | Out-Null
Set-Content -Path $regenFlag -Value "created $(Get-Date -Format s)" -Encoding UTF8
Write-Host "Guard enabled: $regenFlag" -ForegroundColor DarkGray

# 1) Hot backup current state
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$hot = ".archive\HOT_BACKUP_$stamp"
Write-Host "Creating hot backup at $hot"
New-Item -ItemType Directory -Force $hot | Out-Null
if (Test-Path "core\src\retroproto_parsers") {
  Copy-Item -Recurse -Force "core\src\retroproto_parsers" "$hot\retroproto_parsers"
  Write-Host "✓ hot backup copied"
} else {
  Write-Host "i core\src\retroproto_parsers not found (skipping backup copy)" -ForegroundColor DarkGray
}

# 2) Candidate archives (best-first)
$candidates = @(
  "AUTOHEAL_20251106_223110",        # known good from your earlier success
  "INTEGRITY_FIX_20251107_214314",   # top-10 parser fixes
  "FIX_E0425_20251107_220850",       # action shims & E0425 elimination
  "ACTION_REWIRE_20251106_230300",   # actions layout normalized
  "20251106_213325",
  "20251106_213247"
)

# 3) Filter to archives that actually contain a full tree
$full = @()
foreach ($name in $candidates) {
  $p = Join-Path ".archive" $name
  $genMod = Join-Path $p "core\src\retroproto_parsers\generated\mod.rs"
  $reg    = Join-Path $p "core\src\retroproto_parsers\registry.rs"
  if (Test-Path $genMod -and (Test-Path $reg)) { $full += $p }
}
if ($full.Count -eq 0) {
  throw "No archive contains a full retroproto_parsers tree (generated/mod.rs + registry.rs)."
}

# 4) Helper: inject serde import into registry.rs if missing (prevents E0277 cascades)
function Ensure-SerdeImport($regFile) {
  if (-not (Test-Path $regFile)) { return }
  $txt = Get-Content $regFile -Raw
  if ($txt -notmatch 'use\s+serde::\{?\s*Serialize\s*,\s*Deserialize\s*\}?;') {
    $txt = 'use serde::{Serialize, Deserialize};' + "`r`n" + $txt
    Set-Content $regFile -Value $txt -NoNewline -Encoding UTF8
    Write-Host "  (injected serde import into registry.rs)"
  }
}

# 5) Helper: try restore + build
function Try-RestoreAndBuild([string]$srcPath) {
  Write-Section "Trying archive: $srcPath"

  $srcTree = Join-Path $srcPath "core\src\retroproto_parsers"
  if (-not (Test-Path $srcTree)) {
    Write-Host "  (archive missing retroproto_parsers)" -ForegroundColor Yellow
    return $false
  }

  # restore tree
  if (Test-Path "core\src\retroproto_parsers") {
    Remove-Item -Recurse -Force "core\src\retroproto_parsers"
  }
  Copy-Item -Recurse -Force $srcTree "core\src"

  # safety tweak
  Ensure-SerdeImport "core\src\retroproto_parsers\registry.rs"

  # build (stream output and capture exit)
  $log = "build_try_$(Split-Path $srcPath -Leaf)_$(Get-Date -Format yyyyMMdd_HHmmss).log"
  Push-Location core
  try {
    Write-Host "  cargo clean -p dofus-core"
    & cargo clean -p dofus-core | Tee-Object -FilePath $log

    Write-Host "  cargo build --release -p dofus-core"
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "cargo"
    $psi.Arguments = "build --release -p dofus-core"
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError  = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $psi
    [void]$p.Start()
    $stdout = $p.StandardOutput
    $stderr = $p.StandardError

    while (-not $p.HasExited) {
      if (-not $stdout.EndOfStream) {
        $line = $stdout.ReadLine()
        $line | Tee-Object -FilePath $log -Append
        Write-Host $line
      } else {
        Start-Sleep -Milliseconds 50
      }
    }
    # flush remainder
    while (-not $stdout.EndOfStream) { $l=$stdout.ReadLine(); $l | Tee-Object -FilePath $log -Append; Write-Host $l }
    while (-not $stderr.EndOfStream) { $l=$stderr.ReadLine(); $l | Tee-Object -FilePath $log -Append; Write-Host $l }

    $exit = $p.ExitCode
    if ($exit -eq 0) {
      Write-Host "✓ Build succeeded with $srcPath" -ForegroundColor Green
      Write-Host "  Log: core\$log"
      return $true
    } else {
      Write-Host "✗ Build failed with $srcPath (exit $exit)" -ForegroundColor Yellow
      Write-Host "  Log: core\$log"
      return $false
    }
  }
  catch {
    Write-Host "✗ Exception during build: $($_.Exception.Message)" -ForegroundColor Yellow
    return $false
  }
  finally {
    Pop-Location
  }
}

# 6) Iterate candidates until one builds
foreach ($arc in $full) {
  if (Try-RestoreAndBuild $arc) {
    Write-Host ""
    Write-Host "✅ Restored working snapshot: $arc" -ForegroundColor Green
    Write-Host "Guard in place: $regenFlag (prevents accidental codegen)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Next suggested command:" -ForegroundColor Cyan
    Write-Host "  python scripts\run_dummy_pipeline.py --core-only --skip-registry"
    exit 0
  }
}

Write-Host ""
Write-Host "❌ None of the candidate archives built successfully." -ForegroundColor Red
Write-Host "Please share the FIRST error line after running this script so I can target the next fix."
exit 1