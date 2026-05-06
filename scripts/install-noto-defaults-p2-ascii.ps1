# Phase 2 Word + Chrome/Edge - ASCII only + PS 5.1 compatible
$ErrorActionPreference = 'Continue'
Write-Host "=== Phase 2 START ==="

# Word NormalTemplate
Write-Host ""
Write-Host "[Word] NormalTemplate edit"
if (Get-Process WINWORD -ErrorAction SilentlyContinue) {
    Write-Host "  Word running - SKIP"
} else {
    try {
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $doc = $word.Documents.Add()
        $tmpl = $word.NormalTemplate
        $s = $tmpl.Styles.Item(-1)
        $s.Font.NameFarEast = "Noto Sans JP"
        $s.Font.NameAscii = "Noto Sans JP"
        $s.Font.NameOther = "Noto Sans JP"
        $s.Font.Size = 10.5
        $tmpl.Saved = $false
        $tmpl.Save()
        $doc.Close($false)
        $word.Quit()
        [Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
        [GC]::Collect()
        $np = "$env:APPDATA\Microsoft\Templates\Normal.dotm"
        if (Test-Path $np) {
            Write-Host ("  OK: " + (Get-Item $np).Length + " bytes")
        } else {
            Write-Host "  WARN: Normal.dotm not generated"
        }
    } catch {
        Write-Host ("  FAIL: " + $_.Exception.Message)
    }
}

# Browser fonts
function Set-BrowserFonts {
    param([string]$p, [string]$bn, [string]$pn)
    Write-Host ""
    Write-Host ("[" + $bn + "]")
    if (Get-Process $pn -ErrorAction SilentlyContinue) {
        Write-Host ("  " + $bn + " running - stopping")
        Get-Process $pn | Stop-Process -Force
        Start-Sleep -Seconds 2
    }
    if (-not (Test-Path $p)) {
        Write-Host "  Preferences not found - SKIP"
        return
    }
    try {
        $raw = Get-Content $p -Raw -Encoding UTF8
        $j = $raw | ConvertFrom-Json
        if (-not $j.PSObject.Properties['webkit']) {
            $j | Add-Member -MemberType NoteProperty -Name 'webkit' -Value (New-Object PSObject) -Force
        }
        if (-not $j.webkit.PSObject.Properties['webprefs']) {
            $j.webkit | Add-Member -MemberType NoteProperty -Name 'webprefs' -Value (New-Object PSObject) -Force
        }
        if (-not $j.webkit.webprefs.PSObject.Properties['fonts']) {
            $j.webkit.webprefs | Add-Member -MemberType NoteProperty -Name 'fonts' -Value (New-Object PSObject) -Force
        }
        $f = $j.webkit.webprefs.fonts
        $kinds = @('standard','sansserif','serif','fixed')
        foreach ($k in $kinds) {
            if (-not $f.PSObject.Properties[$k]) {
                $f | Add-Member -MemberType NoteProperty -Name $k -Value (New-Object PSObject) -Force
            }
            if ($k -eq 'serif') { $tgt = 'Noto Serif JP' }
            elseif ($k -eq 'fixed') { $tgt = 'Consolas' }
            else { $tgt = 'Noto Sans JP' }
            foreach ($scr in @('Hira','Jpan','Zyyy')) {
                if ($f.$k.PSObject.Properties[$scr]) {
                    $f.$k.$scr = $tgt
                } else {
                    $f.$k | Add-Member -MemberType NoteProperty -Name $scr -Value $tgt -Force
                }
            }
        }
        $newJson = $j | ConvertTo-Json -Depth 100 -Compress
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($p, $newJson, $utf8)
        Write-Host ("  OK: " + $bn + " Preferences updated")
    } catch {
        Write-Host ("  FAIL: " + $_.Exception.Message)
    }
}

Set-BrowserFonts -p "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences" -bn 'Chrome' -pn 'chrome'
Set-BrowserFonts -p "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Preferences" -bn 'Edge' -pn 'msedge'

Write-Host ""
Write-Host "=== Phase 2 DONE ==="
