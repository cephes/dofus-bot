param(
  [switch]$Apply = $false,
  [int]$Limit = 999999
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$py = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

$script = Join-Path $root "tools\cleanup\disable_demo_outputs.py"
if (-not (Test-Path $script)) {
  New-Item -ItemType Directory (Split-Path $script) -Force | Out-Null
  throw "Cleaner not found at $script"
}

Write-Host "== Placeholder/Demo Cleaner ==" -ForegroundColor Cyan
Write-Host "Repo: $root"
Write-Host "Report will be written under .reports/" -ForegroundColor DarkGray

$argsList = @($script, "--limit", "$Limit")
if ($Apply) { $argsList += "--apply" }

Write-Host "Running: $py $($argsList -join ' ')" -ForegroundColor Yellow
& $py @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }