#!/bin/bash
# 会話ログをgitに定期保存
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/.."

if [ -d "takeru-chatbot/logs" ] && ls takeru-chatbot/logs/*.jsonl >/dev/null 2>&1; then
  git add takeru-chatbot/logs/*.jsonl
  if ! git diff --cached --quiet; then
    git commit -m "会話ログ自動保存 $(date '+%Y/%m/%d %H:%M')"
    git push
    echo "ログ保存完了: $(date)"
  fi
fi
