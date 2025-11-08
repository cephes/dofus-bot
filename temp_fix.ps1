$retro = "core\src\retroproto_parsers"

# pick a snapshot that actually contains a full parser tree
$src = Get-ChildItem ".archive" -Directory |
  Sort-Object LastWriteTime -Descending |
  Where-Object {
    (Test-Path (Join-Path $_.FullName "core\src\retroproto_parsers\generated\mod.rs")) -and
    (Test-Path (Join-Path $_.FullName "core\src\retroproto_parsers\registry.rs"))
  } | Select-Object -First 1

if (-not $src) {
  Write-Host "No suitable archive found. Checking for any archive with registry.rs..."
  $src = Get-ChildItem ".archive" -Directory |
    Sort-Object LastWriteTime -Descending |
    Where-Object {
      Test-Path (Join-Path $_.FullName "core\src\retroproto_parsers\registry.rs")
    } | Select-Object -First 1
}

if (-not $src) { throw "No suitable archive under .archive has a full parser tree." }
Write-Host "Restoring from: $($src.FullName)"

# hot backup current state (just in case)
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
New-Item -ItemType Directory ".archive\HOT_BACKUP_$stamp" | Out-Null
Copy-Item -Recurse -Force $retro ".archive\HOT_BACKUP_$stamp\retroproto_parsers"

# restore the entire tree
Copy-Item -Recurse -Force (Join-Path $src.FullName "core\src\retroproto_parsers") "core\src"