# Phase 2: Word Normal.dotm + Chrome/Edge JSON (PS 5.1 互換修正版)
$ErrorActionPreference = 'Continue'
Write-Host "=== Phase 2 (Word + Chrome/Edge fix) ===" -ForegroundColor Cyan

# Word: NormalTemplate API 経由で Normal.dotm を強制生成 + 編集
Write-Host ""
Write-Host "[1/3] Word NormalTemplate -> Noto Sans JP" -ForegroundColor Cyan
if (Get-Process WINWORD -ErrorAction SilentlyContinue) {
    Write-Host "  Word is running - SKIP" -ForegroundColor Yellow
} else {
    try {
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $doc = $word.Documents.Add()
        $tmpl = $word.NormalTemplate
        $style = $tmpl.Styles.Item(-1)
        $style.Font.NameFarEast = "Noto Sans JP"
        $style.Font.NameAscii = "Noto Sans JP"
        $style.Font.NameOther = "Noto Sans JP"
        $style.Font.Size = 10.5
        $tmpl.Saved = $false
        $tmpl.Save()
        $doc.Close($false)
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
        [System.GC]::Collect()
        $normalPath = "$env:APPDATA\Microsoft\Templates\Normal.dotm"
        if (Test-Path $normalPath) {
            $size = (Get-Item $normalPath).Length
            Write-Host "  OK: Normal.dotm Style.Normal = Noto Sans JP, size 10.5pt ($size bytes)" -ForegroundColor Green
        } else {
            Write-Host "  WARN: Normal.dotm not found at $normalPath" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  FAIL: $_" -ForegroundColor Red
    }
}

# Chrome / Edge: PS 5.1 互換で JSON 編集
function Set-BrowserFontsCompat {
    param([string]$prefPath, [string]$browserName, [string]$processName)
    Write-Host ""
    Write-Host "[browser] $browserName" -ForegroundColor Cyan
    if (Get-Process $processName -ErrorAction SilentlyContinue) {
        Write-Host "  $browserName is running - quitting it..." -ForegroundColor Yellow
        Get-Process $processName | Stop-Process -Force
        Start-Sleep -Seconds 2
    }
    if (-not (Test-Path $prefPath)) {
        Write-Host "  Preferences not found - SKIP" -ForegroundColor Yellow
        return
    }
    try {
        $raw = Get-Content $prefPath -Raw -Encoding UTF8
        $json = $raw | ConvertFrom-Json
        # webkit.webprefs.fonts 構造を強制初期化
        if (-not $json.PSObject.Properties['webkit']) {
            $json | Add-Member -MemberType NoteProperty -Name 'webkit' -Value (New-Object PSObject)
        }
        if (-not $json.webkit.PSObject.Properties['webprefs']) {
            $json.webkit | Add-Member -MemberType NoteProperty -Name 'webprefs' -Value (New-Object PSObject)
        }
        if (-not $json.webkit.webprefs.PSObject.Properties['fonts']) {
            $json.webkit.webprefs | Add-Member -MemberType NoteProperty -Name 'fonts' -Value (New-Object PSObject)
        }
        $f = $json.webkit.webprefs.fonts
        foreach ($kind in 'standard','sansserif','serif','fixed') {
            if (-not $f.PSObject.Properties[$kind]) {
                $f | Add-Member -MemberType NoteProperty -Name $kind -Value (New-Object PSObject)
            }
            $target = if ($kind -eq 'serif') { 'Noto Serif JP' } elseif ($kind -eq 'fixed') { 'Consolas' } else { 'Noto Sans JP' }
            foreach ($script in 'Hira','Jpan','Zyyy') {
                if ($f.$kind.PSObject.Properties[$script]) {
                    $f.$kind.$script = $target
                } else {
                    $f.$kind | Add-Member -MemberType NoteProperty -Name $script -Value $target -Force
                }
            }
        }
        $newJson = $json | ConvertTo-Json -Depth 100 -Compress
        [System.IO.File]::WriteAllText($prefPath, $newJson, [System.Text.UTF8Encoding]::new($false))
        Write-Host "  OK: $browserName Preferences updated" -ForegroundColor Green
    } catch {
        Write-Host "  FAIL: $_" -ForegroundColor Red
    }
}

Set-BrowserFontsCompat -prefPath "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences" -browserName 'Chrome' -processName 'chrome'
Set-BrowserFontsCompat -prefPath "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Preferences" -browserName 'Edge' -processName 'msedge'

Write-Host ""
Write-Host "=== Phase 2 DONE ===" -ForegroundColor Cyan
