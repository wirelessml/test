# setup_api_keys.ps1 - 着席後に API キー 3 種を一括永続設定
#
# 使い方:
#   1. ブラウザで以下にサインアップして API キー取得:
#      - ElevenLabs: https://elevenlabs.io/app/settings/api-keys
#      - Groq:       https://console.groq.com/keys
#      - Gemini:     https://aistudio.google.com/app/apikey  (任意)
#   2. PowerShell 管理者権限で本スクリプト実行:
#      powershell -ExecutionPolicy Bypass -File scripts\setup_api_keys.ps1
#   3. 各キーをコピペ入力 (Enter のみで「設定済」をスキップ可能)
#   4. 完了後、新しいターミナルを開いて反映確認

Write-Host "=== 勝間 voice stack API キー一括設定 ===" -ForegroundColor Cyan
Write-Host ""

function Set-ApiKey {
    param([string]$Name, [string]$Url, [string]$Prefix)
    $current = [Environment]::GetEnvironmentVariable($Name, "User")
    $status = if ($current) { "[SET, $($current.Length) chars]" } else { "[NOT SET]" }
    Write-Host "$Name $status" -ForegroundColor Yellow
    Write-Host "  取得元: $Url"
    Write-Host "  接頭辞: $Prefix"
    $key = Read-Host "  キーを貼付け (Enter のみでスキップ)"
    if ($key) {
        [Environment]::SetEnvironmentVariable($Name, $key, "User")
        Write-Host "  -> 永続化完了 (新ターミナル必要)" -ForegroundColor Green
    } else {
        Write-Host "  -> スキップ" -ForegroundColor DarkGray
    }
    Write-Host ""
}

Set-ApiKey -Name "ELEVENLABS_API_KEY" -Url "https://elevenlabs.io/app/settings/api-keys" -Prefix "sk_..."
Set-ApiKey -Name "GROQ_API_KEY" -Url "https://console.groq.com/keys" -Prefix "gsk_..."
Set-ApiKey -Name "GEMINI_API_KEY" -Url "https://aistudio.google.com/app/apikey" -Prefix "AIza..."

Write-Host "=== 完了 ===" -ForegroundColor Cyan
Write-Host "新しい PowerShell を開いて以下で確認:"
Write-Host '  echo $env:ELEVENLABS_API_KEY'
Write-Host '  echo $env:GROQ_API_KEY'
Write-Host '  echo $env:GEMINI_API_KEY'
Write-Host ""
Write-Host "動作確認:" -ForegroundColor Cyan
Write-Host "  python C:\Users\gci_admin\voice-stack\scripts\scribe_api.py --check"
Write-Host "  python C:\Users\gci_admin\voice-stack\scripts\scribe_kanjisuji_fix.py --check"
