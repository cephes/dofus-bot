param(
    [switch]$SkipRegistry,
    [switch]$CoreOnly,
    [switch]$NoStop
)
$flags = @()
if ($SkipRegistry) { $flags += "--skip-registry" }
if ($CoreOnly) { $flags += "--core-only" }
if ($NoStop) { $flags += "--no-stop" }

Write-Host "Running pipeline with flags: $($flags -join ' ')" -ForegroundColor Cyan
Write-Host "Command: python scripts\run_dummy_pipeline.py $($flags -join ' ')" -ForegroundColor Yellow
Write-Host ""

python scripts\run_dummy_pipeline.py @flags