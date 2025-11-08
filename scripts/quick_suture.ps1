# scripts/quick_suture.ps1
$ErrorActionPreference = 'Stop'

$genDir   = "core/src/retroproto_parsers/generated"
$actDir   = Join-Path $genDir "actions"
$modFile  = Join-Path $actDir "mod.rs"

# 0) Safety backup
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$bak   = ".archive/QUICK_SUTURE_$stamp"
New-Item -ItemType Directory -Force -Path $bak | Out-Null
Copy-Item $genDir -Destination $bak -Recurse -Force

# 1) Patch all generated .rs files
$files = Get-ChildItem $genDir -Recurse -Filter *.rs

foreach ($f in $files) {
  $src = Get-Content $f.FullName -Raw

  # a) reserved keyword double-hash: r#r#type  -> r#type
  $src = $src -replace 'r#r#type', 'r#type'

  # b) pathological repeated label: r#type: r#type: ... -> r#type:
  $src = $src -replace '(r#type:\s*){2,}', 'r#type: '

  # c) struct literal started with a stray comma:
  #    `{, ..Default::default()}` -> `{ ..Default::default() }`
  $src = $src -replace '\{\s*,\s*\.\.\s*Default::default\(\)\s*\}', '{ ..Default::default() }'

  # d) double commas in field lists: ",," -> ", "
  #    repeat a couple of times to be safe
  for ($i=0; $i -lt 3; $i++) {
    $src = $src -replace ',\s*,', ', '
  }

  # e) lines like "field,, ..Default::default()" -> "field, ..Default::default()"
  $src = $src -replace ',\s*,\s*\.\.\s*Default::default\(\)', ', ..Default::default()'

  # f) stray derive placed before a use (invalid position):
  #    If a #[derive(...)] is immediately followed by a `use serde::`, drop the derive.
  $src = $src -replace '(?ms)^\s*#\s*\[\s*derive[^\]]*\]\s*\r?\n\s*(use\s+serde::\{?Serialize,\s*Deserialize\}?\s*;)', '$1'

  # g) common typo: `serde:: Deserialize` (extra space after ::)
  $src = $src -replace 'serde::\s+Deserialize', 'serde::Deserialize'

  Set-Content -Path $f.FullName -Value $src -NoNewline
}

# 2) Make sure actions:: modules exist (fixes E0432)
$needed = @(
  'pub mod GameAction_1;',
  'pub mod GameAction_2;',
  'pub mod GameAction_900;',
  'pub mod GameAction_901;',
  'pub mod GameAction_902;',
  'pub mod GameAction_903;'
)

if (Test-Path $modFile) {
  $modTxt = Get-Content $modFile -Raw
  $changed = $false
  foreach ($line in $needed) {
    if ($modTxt -notmatch [regex]::Escape($line)) {
      $modTxt += "`r`n$line"
      $changed = $true
    }
  }
  if ($changed) { Set-Content -Path $modFile -Value $modTxt }
}

Write-Host "Quick suture done. Rebuilding..." -ForegroundColor Cyan
# Rebuild; tee to a timestamped log
$buildLog = "core/build_after_suture.log"
pushd core
try {
  cargo build --release -p dofus-core 2>&1 | Tee-Object -FilePath $buildLog
} finally {
  popd
}
Write-Host "Build log: $buildLog" -ForegroundColor Yellow

# Show a compact error summary (top codes)
Select-String -Path $buildLog -Pattern "error\[E\d{4}\]" |
  ForEach-Object { [regex]::Match($_.Line, "E\d{4}").Value } |
  Group-Object | Sort-Object Count -Desc | Format-Table Name,Count
