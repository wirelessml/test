# Force-update Claude Code on Windows by downloading GitHub release zip
$ErrorActionPreference = 'Continue'
$ver = '2.1.129'
$url = "https://github.com/anthropics/claude-code/releases/download/v$ver/claude-win32-x64.zip"
$zip = "$env:TEMP\claude-$ver.zip"
$ext = "$env:TEMP\claude-$ver"
$dst = "$env:USERPROFILE\.local\bin"

Write-Host "Before:"
claude --version 2>&1

Write-Host ""
Write-Host "Downloading $url"
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
Write-Host ("  zip size: " + (Get-Item $zip).Length + " bytes")

if (Test-Path $ext) { Remove-Item -Recurse -Force $ext -ErrorAction SilentlyContinue }
Expand-Archive -Path $zip -DestinationPath $ext -Force
Write-Host "  extracted"

# Find claude.exe inside extracted dir
$exes = Get-ChildItem $ext -Recurse -Filter 'claude*.exe'
Write-Host ("  found " + $exes.Count + " exe(s):")
foreach ($e in $exes) {
    Write-Host ("    " + $e.FullName)
}

# Copy all binaries to destination
foreach ($e in $exes) {
    $dest = Join-Path $dst $e.Name
    Copy-Item -Path $e.FullName -Destination $dest -Force
    Write-Host ("  copied " + $e.Name + " -> " + $dest)
}

Write-Host ""
Write-Host "After:"
claude --version 2>&1
