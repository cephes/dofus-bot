Write-Host "== Generating action shims =="
python tools\ensure_action_shims.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "== Building core =="
cargo build --release -p dofus-core
exit $LASTEXITCODE