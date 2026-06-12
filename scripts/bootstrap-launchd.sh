#!/bin/bash
# bootstrap-launchd.sh — Mac 喪失/再セットアップ時に launchd 常駐インフラを git から復元する
#
# 背景: 2026-06-12 の TCC 罠対策で、稼働実体は ~/Library/Application Support/<name>/ に在り
#       git には正本（scripts/ と config/launchagents/）だけが残る構成になった。
#       Mac が死んだ場合・新 Mac 移行時に、この 1 本で常駐群を再組み立てする。
#
# 使い方:
#   bash scripts/bootstrap-launchd.sh check     # 現状と git 正本の一致を検査（変更なし）
#   bash scripts/bootstrap-launchd.sh install   # plist 配置 + App Support 組み立て + bootstrap
#
# ⚠️ git に入っていないもの（install 後に手動で用意）:
#   1. ~/.config/masu-p-watch/email.json     … Gmail アプリパスワード（chmod 600）
#   2. scripts/kanno-watch.sh                … ローカル保持判断（6/12）のため git 外。旧 Mac から手動コピー
#   3. ~/whisper-models/ggml-large-v3-turbo.bin … 1.5GB、再DL
#   4. BlackHole 2ch + Audio MIDI「複数出力装置」 … 録画系の前提
#   5. Terminal の Full Disk Access / TCC 承認類
#   6. gh auth login（job-report の wirelessml/job-hunt-reports push 用）
set -u
MODE="${1:-check}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LA="$HOME/Library/LaunchAgents"
AS="$HOME/Library/Application Support"
fail=0; warn=0

# 組み立て表: "App Support 相対パス|repo 相対パス"
ASSEMBLY="
kanno-watch/kanno-watch.sh|scripts/kanno-watch.sh
kanno-watch/lib/send-email.py|scripts/lib/send-email.py
kioxia-monitor/amazon-kioxia-monitor.sh|scripts/amazon-kioxia-monitor.sh
masu-p-watch/masu-p-watch.sh|scripts/masu-p-watch.sh
masu-p-watch/lib/send-email.py|scripts/lib/send-email.py
reco-ollama-mock/reco-ollama-mock.py|scripts/reco-ollama-mock.py
job-report/job-search-daily.py|scripts/job-search-daily-mac.py
job-report/email-job-report.sh|scripts/email-job-report.sh
job-report/send-email.py|scripts/lib/send-email.py
"

check_or_install_file() { # $1=対象(絶対) $2=正本(絶対)
  local dst="$1" src="$2"
  if [ ! -f "$src" ]; then
    echo "⚠️  正本が git 外: ${src#$REPO/} （手動コピー対象。ヘッダの注意書き参照）"
    warn=$((warn+1)); return
  fi
  if [ "$MODE" = "install" ]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst" && chmod +x "$dst"
    echo "📦 installed: ${dst#$HOME/}"
  else
    if [ ! -f "$dst" ]; then
      echo "🚨 未配置: ${dst#$HOME/}"; fail=1
    elif ! diff -q "$src" "$dst" >/dev/null 2>&1; then
      echo "🚨 drift: ${dst#$HOME/} が正本 ${src#$REPO/} と不一致"; fail=1
    else
      echo "✅ ${dst#$HOME/}"
    fi
  fi
}

echo "== bootstrap-launchd (${MODE}) $(LC_ALL=C date '+%F %T') =="

# 1) plist
for p in "$REPO"/config/launchagents/*.plist; do
  base="$(basename "$p")"
  label="${base%.plist}"
  if [ "$MODE" = "install" ]; then
    cp "$p" "$LA/$base"
    launchctl bootout "gui/$(id -u)/$label" 2>/dev/null
    launchctl bootstrap "gui/$(id -u)" "$LA/$base" && echo "📦 bootstrapped: ${label}"
  else
    if [ ! -f "$LA/$base" ]; then
      echo "🚨 plist 未配置: ${base}"; fail=1
    elif ! diff -q "$p" "$LA/$base" >/dev/null 2>&1; then
      echo "🚨 plist drift: ${base}（repo と実機で差分）"; fail=1
    else
      echo "✅ plist ${base}"
    fi
  fi
done

# 2) App Support 組み立て
echo "$ASSEMBLY" | while IFS='|' read -r rel src; do
  [ -n "$rel" ] || continue
  check_or_install_file "$AS/$rel" "$REPO/$src"
done
# while がサブシェルのため fail を拾い直す（check 時のみ厳密化）
if [ "$MODE" = "check" ]; then
  bad=$(echo "$ASSEMBLY" | while IFS='|' read -r rel src; do
    [ -n "$rel" ] || continue
    [ -f "$REPO/$src" ] || continue
    { [ -f "$AS/$rel" ] && diff -q "$REPO/$src" "$AS/$rel" >/dev/null 2>&1; } || echo NG
  done | grep -c NG)
  [ "$bad" -gt 0 ] && fail=1
fi

# 3) スナップショット等の器
if [ "$MODE" = "install" ]; then
  mkdir -p "$AS/masu-p-watch/snapshots"
  echo ""
  echo "次: launchagent-doctor で健全性確認 →  bash scripts/launchagent-doctor.sh"
  echo "⚠️ ヘッダ記載の手動 6 項目（email.json / kanno-watch.sh / whisper モデル / BlackHole / TCC / gh auth）を忘れずに"
fi

echo "== 結果: $([ $fail -eq 0 ] && echo "OK ✅" || echo "NG 🚨")（警告 ${warn} 件）=="
exit $fail
