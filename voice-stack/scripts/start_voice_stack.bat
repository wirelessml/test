@echo off
REM start_voice_stack.bat - 無変換キー Scribe 常駐起動
REM
REM 使い方:
REM   - ダブルクリックで keybind_scribe.py を非表示で常駐起動
REM   - スタートアップフォルダ (shell:startup) に置けばログイン時自動起動
REM
REM 詳細:
REM   - keybind_scribe.py: 無変換キー長押し → Scribe → 漢数字補正 → クリップボード+貼付
REM   - キーボードフックは管理者権限不要で動作

cd /d C:\Users\gci_admin\voice-stack\scripts
start "voice-stack" /MIN pythonw keybind_scribe.py
