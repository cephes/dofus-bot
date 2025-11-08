$ErrorActionPreference = 'Stop'

$path = 'dofus-retro-bot\third_party\retroproto'
$gitDir = Join-Path $path '.git'
if (!(Test-Path $gitDir)) {
  Write-Host "No nested .git found at $gitDir — nothing to do." -ForegroundColor Yellow
  return
}

# 1) Make a safety archive
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$arch  = ".archive\RETROPROTO_NESTED_$stamp"
New-Item -ItemType Directory -Force -Path $arch | Out-Null

# 2) Capture useful info (remote + commit)
try {
  $remote = git -C $path remote -v 2>$null
  if ($LASTEXITCODE -eq 0) { $remote | Out-File -Encoding utf8 (Join-Path $arch 'remote.txt') }
} catch { }

try {
  $sha = git -C $path rev-parse HEAD 2>$null
  if ($LASTEXITCODE -eq 0) { $sha | Out-File -Encoding utf8 (Join-Path $arch 'commit.txt') }
} catch { }

# 3) Back up the nested .git directory itself
Copy-Item -Recurse -Force $gitDir (Join-Path $arch '.git_backup')

# 4) Remove the nested repo metadata so tools stop seeing it
Remove-Item -Recurse -Force $gitDir

# 5) (Optional) Prevent accidental re-introduction
Add-Content -Path '.gitignore' -Value 'dofus-retro-bot/third_party/retroproto/.git'

Write-Host "Nested Git removed. Backup at $arch" -ForegroundColor Green

# 6) Verify
if (Test-Path $gitDir) {
  Write-Host "ERROR: .git still present." -ForegroundColor Red
} else {
  Write-Host "Success: no nested .git detected" -ForegroundColor Green
}