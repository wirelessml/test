#!/bin/bash
# Role: 毎朝、masupが04:00に生成しGitHubへpushした求人レポートを公開rawから取得し、メール送信する。
#        Mac既存の send-email.py（~/.config/masu-p-watch/email.json のapp password）を再利用。ssh不要・常駐しない一発ジョブ。
set -u
LOG="$HOME/Desktop/scripts/job-report-email.log"
REP="/tmp/job-report-latest.md"
DATE="$(date +%F)"
RAWBASE="https://raw.githubusercontent.com/wirelessml/job-hunt-reports/main/reports"
GH="/opt/homebrew/bin/gh"
PY="/usr/bin/python3"

# 1) 当日分を公開rawから取得（masupが既にpush済みのはず）
/usr/bin/curl -fsSL "$RAWBASE/job-report-${DATE}.md" -o "$REP" 2>/dev/null
# 2) 無ければ最新ファイル名をghで引いて取得（フォールバック）
if [ ! -s "$REP" ]; then
  latest="$("$GH" api repos/wirelessml/job-hunt-reports/contents/reports --jq 'map(.name)|sort|last' 2>/dev/null | tr -d '"')"
  [ -n "$latest" ] && /usr/bin/curl -fsSL "$RAWBASE/$latest" -o "$REP" 2>/dev/null
fi
if [ ! -s "$REP" ]; then echo "$(date '+%F %T') NO_REPORT (GitHub未取得)" >> "$LOG"; exit 1; fi

total="$(grep -m1 '合計' "$REP" | grep -oE '[0-9]+' | head -1)"
SUBJECT="【就活求人レポート】${DATE} 計${total:-?}件（戎町500m＋本社=兵庫/大阪/京都リモート, 同志社/将棋優先）"
"$PY" "$HOME/Desktop/scripts/lib/send-email.py" --subject "$SUBJECT" --body-file "$REP" >> "$LOG" 2>&1
echo "$(date '+%F %T') sent rc=$? subject=$SUBJECT" >> "$LOG"
