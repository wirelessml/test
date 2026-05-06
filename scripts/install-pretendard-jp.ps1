# Pretendard JP install only (no FontSubstitutes change)
$ErrorActionPreference = 'Continue'
Write-Host "=== Pretendard JP install ==="
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host ("IsAdmin: " + $isAdmin)

$ver = '1.3.9'
$urls = @(
    "https://github.com/orioncactus/pretendard/releases/download/v$ver/PretendardJP-$ver.zip",
    "https://github.com/orioncactus/pretendard/releases/download/v$ver/PretendardJPVariable-$ver.zip"
)
$fontDir = "C:\Windows\Fonts"
$regKey = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
$copied = 0
$skipped = 0

foreach ($url in $urls) {
    $name = Split-Path $url -Leaf
    $zip = "$env:TEMP\$name"
    $ext = "$env:TEMP\" + ($name -replace '\.zip$', '')
    Write-Host ""
    Write-Host ("Downloading " + $url)
    try {
        Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
        $size = (Get-Item $zip).Length
        Write-Host ("  size: " + $size + " bytes")
    } catch {
        Write-Host ("  download FAIL: " + $_.Exception.Message)
        continue
    }
    try {
        if (Test-Path $ext) { Remove-Item -Recurse -Force $ext -ErrorAction SilentlyContinue }
        Expand-Archive -Path $zip -DestinationPath $ext -Force
    } catch {
        Write-Host ("  extract FAIL: " + $_.Exception.Message)
        continue
    }
    $fonts = Get-ChildItem $ext -Recurse -Include *.ttf,*.otf -ErrorAction SilentlyContinue
    Write-Host ("  found " + $fonts.Count + " font file(s)")
    foreach ($f in $fonts) {
        $dst = Join-Path $fontDir $f.Name
        if (Test-Path $dst) {
            $skipped++
            continue
        }
        try {
            Copy-Item -Path $f.FullName -Destination $dst -Force -ErrorAction Stop
            $regName = $f.BaseName + ' (TrueType)'
            Set-ItemProperty -Path $regKey -Name $regName -Value $f.Name -Type String -ErrorAction SilentlyContinue
            $copied++
        } catch {
            Write-Host ("    fail " + $f.Name + ": " + $_.Exception.Message)
        }
    }
}

Write-Host ""
Write-Host ("=== installed: " + $copied + ", skipped (already exists): " + $skipped + " ===")

# Verify
Write-Host ""
Write-Host "=== Pretendard fonts in C:\Windows\Fonts ==="
Get-ChildItem $fontDir -Filter Pretendard* | Select-Object Name | Format-Table -AutoSize
