#!/bin/bash
# SessionStart hook: 「枠の頭で計画」ルール (docs/rules/session-setup.md, 6/10制定) の自動化。
# セッション開始時に時刻・枠プラン要求・最新ジャーナルの未完了事項を context に注入する。
# Windows checkout でも害がないよう Darwin 以外は即終了。
[ "$(uname)" = "Darwin" ] || exit 0

now=$(LC_ALL=C date '+%Y-%m-%d %H:%M (%a)')
echo "[枠の頭で計画] 現在 ${now} JST. 新しい5時間枠の可能性あり。冒頭で「この枠のプラン」を3行提示すること（①この枠の優先タスク1-2個 ②重い処理の有無→あるなら枠の前半に配置 ③前枠からの持ち越し）。"

dir="${CLAUDE_PROJECT_DIR:-$HOME/Desktop}/docs/journal"
latest=$(ls "$dir"/2026-*.md 2>/dev/null | sort | tail -1)
if [ -n "$latest" ]; then
  echo "最新ジャーナル: ${latest##*/} の未完了/持ち越し:"
  awk '/^## (未完了|次のステップ)/{f=1;next} f&&/^## /{exit} f&&NF' "$latest" | head -8
fi
exit 0
