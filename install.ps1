# Workspace 2.0 installer: skill + slash commands + output style -> ~/.claude
$ErrorActionPreference = 'Stop'
$src  = $PSScriptRoot
$dest = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE '.claude' }
foreach ($d in 'skills', 'commands', 'output-styles') { New-Item -ItemType Directory -Force (Join-Path $dest $d) | Out-Null }
$skill = Join-Path $dest 'skills\workspace-2'
$models = Join-Path $skill 'scripts\models.json'
$kept = $null
if (Test-Path $models) { $kept = [IO.Path]::GetTempFileName(); Copy-Item -Force $models $kept }
if (Test-Path $skill) { Remove-Item -Recurse -Force $skill }
Copy-Item -Recurse (Join-Path $src 'skill\workspace-2') (Join-Path $dest 'skills')
if ($kept) { Move-Item -Force $kept $models; Write-Host 'Kept your models.json' }
Copy-Item (Join-Path $src 'commands\*.md') (Join-Path $dest 'commands')
Copy-Item (Join-Path $src 'output-styles\*.md') (Join-Path $dest 'output-styles')
Write-Host "Installed to $dest"
Write-Host "Next: set model ids in $skill\scripts\models.json"
Write-Host "Optional: pick output style 'Workspace Terse' (/output-style, or the app's settings)"
Write-Host "Type /ws in Claude Code to see the commands."
