(Get-Content core\src\retroproto_parsers\generated\mod.rs -Raw) `
  -replace '^\s*pub use actions::GameActions\w*::\*;\s*$', '' |
  Set-Content core\src\retroproto_parsers\generated\mod.rs