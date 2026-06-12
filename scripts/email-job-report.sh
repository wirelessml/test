#!/bin/bash
# Role: 毎朝、masupが04:00に生成しGitHubへpushした求人レポートを公開rawから取得し、メール送信する。
#        send-email.py（~/.config/masu-p-watch/email.json のapp password）を再利用。ssh不要・常駐しない一発ジョブ。
# 注: launchdが ~/Desktop をTCCで読めない問題(戻り値126)を回避するため、
#     本ジョブ一式は ~/Library/Application Support/job-report/ に配置（2026-06-07 移設）。
set -u
SELF_DIR="$HOME/Library/Application Support/job-report"
LOG="$SELF_DIR/job-report-email.log"
# 同日の二重送信防止（04:30生成ジョブが送信済みなら05:00ジョブはスキップ）
MARKER="$SELF_DIR/last-emailed-date.txt"
if [ -f "$MARKER" ] && [ "$(cat "$MARKER" 2>/dev/null)" = "$(date +%F)" ]; then
  echo "$(date '+%F %T') SKIP (already emailed today)" >> "$LOG"; exit 0
fi
SENDER="$SELF_DIR/send-email.py"
REP="/tmp/job-report-latest.md"
DATE="$(date +%F)"
RAWBASE="https://raw.githubusercontent.com/wirelessml/job-hunt-reports/main/reports"
GH="/opt/homebrew/bin/gh"
PY="/usr/bin/python3"

# 1) 当日分を公開rawから取得（masupが既にpush済みのはず）
/usr/bin/curl -fsSL "$RAWBASE/job-report-${DATE}.md" -o "$REP" 2>/dev/null
STALE=""
# 2) 無ければ最新ファイル名をghで引いて取得（フォールバック。件名には実レポート日付＋古い旨を明記）
if [ ! -s "$REP" ]; then
  latest="$("$GH" api repos/wirelessml/job-hunt-reports/contents/reports --jq 'map(.name)|sort|last' 2>/dev/null | tr -d '"')"
  if [ -n "$latest" ]; then
    /usr/bin/curl -fsSL "$RAWBASE/$latest" -o "$REP" 2>/dev/null
    repdate="$(echo "$latest" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
    [ -n "$repdate" ] && [ "$repdate" != "$DATE" ] && STALE="⚠️${repdate}分の再送(当日分未生成)・"
  fi
fi
if [ ! -s "$REP" ]; then echo "$(date '+%F %T') NO_REPORT (GitHub未取得)" >> "$LOG"; exit 1; fi

total="$(grep -m1 '合計' "$REP" | grep -oE '[0-9]+' | head -1)"
SUBJECT="【就活求人レポート】${DATE} ${STALE}計${total:-?}件（板宿駅1km・資格不要＋声を出さない在宅事務）"
"$PY" "$SENDER" --subject "$SUBJECT" --body-file "$REP" >> "$LOG" 2>&1
rc=$?
[ $rc -eq 0 ] && [ -z "$STALE" ] && date +%F > "$MARKER"
echo "$(date '+%F %T') sent rc=$rc subject=$SUBJECT" >> "$LOG"
