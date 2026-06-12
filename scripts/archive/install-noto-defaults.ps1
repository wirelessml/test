#Requires -Version 5.1
# Noto Sans JP をしゅん先生 PC のデフォルトフォントに設定する全レイヤースクリプト
# 2026-05-06 作成 by Claude Code (Mac M1) for 仲啓輔
# 戻し方: $env:USERPROFILE\Desktop\font-default-backup-2026-05-06\ 内の .reg / Normal.dotm / Preferences.json を復元

$ErrorActionPreference = 'Continue'
$ts = Get-Date -Format 'HH:mm:ss'
Write-Host "=== Noto Default Font Installer (start $ts) ===" -ForegroundColor Cyan

# 0. Admin check
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host "IsAdmin: $isAdmin" -ForegroundColor $(if($isAdmin){'Green'}else{'Yellow'})

# 1. Backup
$backupDir = "$env:USERPROFILE\Desktop\font-default-backup-2026-05-06"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Write-Host ""
Write-Host "[1/5] Backup -> $backupDir" -ForegroundColor Cyan
reg export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes" "$backupDir\FontSubstitutes.reg" /y 2>&1 | Out-Null
reg export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "$backupDir\Fonts.reg" /y 2>&1 | Out-Null
Copy-Item "$env:APPDATA\Microsoft\Templates\Normal.dotm" "$backupDir\Normal.dotm" -Force -ErrorAction SilentlyContinue
Copy-Item "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences" "$backupDir\chrome-Preferences.json" -Force -ErrorAction SilentlyContinue
Copy-Item "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Preferences" "$backupDir\edge-Preferences.json" -Force -ErrorAction SilentlyContinue
Get-ChildItem $backupDir | Format-Table Name, Length -AutoSize

# 2. Word Normal.dotm
Write-Host ""
Write-Host "[2/5] Word Normal.dotm -> Noto Sans JP" -ForegroundColor Cyan
if (Get-Process WINWORD -ErrorAction SilentlyContinue) {
    Write-Host "  Word is running - SKIP. Close Word and re-run for this layer." -ForegroundColor Yellow
} else {
    try {
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $normalPath = "$env:APPDATA\Microsoft\Templates\Normal.dotm"
        $doc = $word.Documents.Open($normalPath)
        $style = $doc.Styles.Item(-1)  # wdStyleNormal
        $style.Font.NameFarEast = "Noto Sans JP"
        $style.Font.NameAscii = "Noto Sans JP"
        $style.Font.NameOther = "Noto Sans JP"
        $style.Font.Size = 10.5
        $doc.Save()
        $doc.Close()
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
        [System.GC]::Collect()
        Write-Host "  OK: Normal.dotm body font = Noto Sans JP, size 10.5pt" -ForegroundColor Green
    } catch {
        Write-Host "  FAIL: $_" -ForegroundColor Red
    }
}

# 3. Excel registry
Write-Host ""
Write-Host "[3/5] Excel default font (HKCU)" -ForegroundColor Cyan
$excelVer = '16.0'  # Office 2016+/365
$excelKey = "HKCU:\Software\Microsoft\Office\$excelVer\Excel\Options"
if (-not (Test-Path $excelKey)) { New-Item -Path $excelKey -Force | Out-Null }
Set-ItemProperty -Path $excelKey -Name 'Font' -Value 'Noto Sans JP, 11' -Type String
Write-Host "  OK: $excelKey\Font = 'Noto Sans JP, 11'" -ForegroundColor Green

# 4. Chrome / Edge font preferences (only when not running)
Write-Host ""
Write-Host "[4/5] Chrome / Edge font preferences" -ForegroundColor Cyan
function Set-BrowserFonts {
    param([string]$prefPath, [string]$browserName, [string]$processName)
    if (Get-Process $processName -ErrorAction SilentlyContinue) {
        Write-Host "  ${browserName}: running - SKIP, set manually at chrome://settings/fonts" -ForegroundColor Yellow
        return
    }
    if (-not (Test-Path $prefPath)) {
        Write-Host "  ${browserName}: Preferences not found - SKIP" -ForegroundColor Yellow
        return
    }
    try {
        $raw = Get-Content $prefPath -Raw -Encoding UTF8
        $json = $raw | ConvertFrom-Json -Depth 100
        if (-not $json.webkit) { $json | Add-Member -MemberType NoteProperty -Name 'webkit' -Value ([ordered]@{}) -Force }
        if (-not $json.webkit.webprefs) { $json.webkit | Add-Member -MemberType NoteProperty -Name 'webprefs' -Value ([ordered]@{}) -Force }
        if (-not $json.webkit.webprefs.fonts) { $json.webkit.webprefs | Add-Member -MemberType NoteProperty -Name 'fonts' -Value ([ordered]@{}) -Force }
        $f = $json.webkit.webprefs.fonts
        foreach ($kind in 'standard','sansserif','serif') {
            if (-not $f.$kind) { $f | Add-Member -MemberType NoteProperty -Name $kind -Value ([ordered]@{}) -Force }
            $target = if ($kind -eq 'serif') { 'Noto Serif JP' } else { 'Noto Sans JP' }
            $f.$kind | Add-Member -MemberType NoteProperty -Name 'Hira' -Value $target -Force
            $f.$kind | Add-Member -MemberType NoteProperty -Name 'Jpan' -Value $target -Force
            $f.$kind | Add-Member -MemberType NoteProperty -Name 'Zyyy' -Value $target -Force
        }
        $json | ConvertTo-Json -Depth 100 -Compress | Set-Content $prefPath -Encoding UTF8
        Write-Host "  ${browserName}: OK" -ForegroundColor Green
    } catch {
        Write-Host "  ${browserName} edit FAIL: $_" -ForegroundColor Red
    }
}
Set-BrowserFonts -prefPath "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences" -browserName 'Chrome' -processName 'chrome'
Set-BrowserFonts -prefPath "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Preferences" -browserName 'Edge' -processName 'msedge'

# 5. System UI (HKLM\FontSubstitutes) - requires admin + reboot
Write-Host ""
Write-Host "[5/5] System UI FontSubstitutes (HKLM, requires admin + reboot)" -ForegroundColor Cyan
if (-not $isAdmin) {
    Write-Host "  Not admin - SKIP. Re-run from elevated shell." -ForegroundColor Yellow
} else {
    $key = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes'
    $subs = @(
        'Yu Gothic UI',
        'Yu Gothic UI Bold',
        'Yu Gothic UI Italic',
        'Yu Gothic UI Light',
        'Yu Gothic UI Semibold',
        'Yu Gothic UI Semilight',
        'Meiryo UI',
        'Meiryo UI Bold',
        'MS UI Gothic',
        'MS Gothic',
        'MS PGothic'
    )
    foreach ($name in $subs) {
        Set-ItemProperty -Path $key -Name $name -Value 'Noto Sans JP' -Type String -ErrorAction SilentlyContinue
    }
    Write-Host "  OK: $($subs.Count) Japanese UI fonts mapped to Noto Sans JP (REBOOT required)" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Cyan
Write-Host "Backup at: $backupDir"
Write-Host "Reboot required for System UI changes to take effect."
Write-Host "To revert system UI: reg import $backupDir\FontSubstitutes.reg && reboot"
