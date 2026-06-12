$ErrorActionPreference = 'Stop'
$ver = '2.1.145'
$url = "https://github.com/anthropics/claude-code/releases/download/v$ver/claude-win32-x64.zip"
$zip = "$env:TEMP\claude-$ver.zip"
$extract = "$env:TEMP\claude-$ver-extracted"
$dest = "$env:USERPROFILE\.local\bin\claude.exe"

Write-Output "Downloading $url"
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing

if (Test-Path $extract) { Remove-Item $extract -Recurse -Force }
Expand-Archive -Path $zip -DestinationPath $extract -Force

$srcExe = Get-ChildItem $extract -Filter claude.exe -Recurse | Select-Object -First 1
if (-not $srcExe) { throw "claude.exe not found in zip" }

Copy-Item $srcExe.FullName -Destination $dest -Force
Write-Output "--- installed ---"
& $dest --version
