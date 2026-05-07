#!/usr/bin/env bash
# Watch openai/codex PR #21206 (tui-pets) merge状態。
# merged されたら macOS notification + flag file + log 記録。

set -u
LOG=/Users/yuika/Desktop/docs/routines/codex-tui-pets-watch-log.md
FLAG=/Users/yuika/Desktop/docs/routines/codex-tui-pets-merged.flag

ts=$(date '+%Y-%m-%d %H:%M:%S %Z')

# Ensure log file exists with header
if [[ ! -f "$LOG" ]]; then
    mkdir -p "$(dirname "$LOG")"
    cat > "$LOG" <<'HDR'
# Codex TUI pets PR (#21206) Watch Log

PR: https://github.com/openai/codex/pull/21206
Branch: tui-pets
Schedule: 毎日 10:17 JST (LaunchAgent com.yuika.codex-tui-pets-watch)

## 監視ログ

HDR
fi

# Check PR state via gh CLI
state=$(gh pr view 21206 --repo openai/codex --json state --jq '.state' 2>&1)
merged=$(gh pr view 21206 --repo openai/codex --json mergedAt --jq '.mergedAt' 2>&1)
updated=$(gh pr view 21206 --repo openai/codex --json updatedAt --jq '.updatedAt' 2>&1)

if [[ "$state" == "MERGED" && ! -f "$FLAG" ]]; then
    # 初回検出
    {
        echo ""
        echo "## $ts 🎉 MERGED"
        echo "- PR #21206 (tui-pets) merged at $merged"
        echo "- 次のステップ: codex-alpha 再 download (latest tag) → TUI で codex-alpha 起動 → shibu pet が composer 周辺に出現するか確認"
    } >> "$LOG"
    touch "$FLAG"
    # macOS 通知
    osascript -e 'display notification "PR #21206 (tui-pets) が main にマージされました。codex-alpha を再 install して TUI pets を試せます。" with title "Codex TUI pets 配信開始 🎉" sound name "Glass"' 2>/dev/null || true
elif [[ "$state" == "MERGED" ]]; then
    echo "- $ts merged-already (no notify, flag exists)" >> "$LOG"
elif [[ "$state" == "OPEN" ]]; then
    echo "- $ts OPEN (last_update=$updated, waiting)" >> "$LOG"
else
    echo "- $ts state=$state (unexpected, raw=\"$state\")" >> "$LOG"
fi
