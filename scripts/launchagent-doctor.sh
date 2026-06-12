#!/bin/bash
# launchagent-doctor — LaunchAgent 健全性チェック
#
# 背景（再発防止の対象）:
#   - 2026-06-10: 「全て終了」の巻き添えで LaunchAgent 7 個が全アンロードされた事故
#   - 2026-06-07: launchd の TCC 罠（~/Desktop 配下のスクリプトを launchd から実行すると
#     Operation not permitted / exit 126）で就活メールが 2 日間不達
#
# チェック内容:
#   1. ~/Library/LaunchAgents/*.plist（サードパーティ updater 除く）が全てロード済みか
#   2. ロード済みジョブの最終 exit status が 0 か
#   3. .disabled にした plist が復活していないか
#   4. launchd 起動物が ~/Desktop 配下を参照していないか（TCC 罠）
#   5. scripts/launchagents-expected.txt（あれば）との突合
#
# 使い方: bash scripts/launchagent-doctor.sh   （exit 0=健全 / 1=要対応あり）
set -u
LA_DIR="$HOME/Library/LaunchAgents"
MANIFEST="$(cd "$(dirname "$0")" && pwd)/launchagents-expected.txt"
fail=0; warn=0

loaded=$(launchctl list 2>/dev/null)

echo "== launchagent-doctor $(LC_ALL=C date '+%F %T') =="

# 1+2) インストール済み plist のロード状態と exit status
for p in "$LA_DIR"/*.plist; do
  [ -e "$p" ] || continue
  label=$(/usr/libexec/PlistBuddy -c 'Print :Label' "$p" 2>/dev/null) || label=$(basename "$p" .plist)
  case "$label" in
    com.google.*|com.microsoft.*|com.valvesoftware.*) continue ;;
  esac
  line=$(printf '%s\n' "$loaded" | awk -v l="$label" '$3==l')
  if [ -n "$line" ]; then
    status=$(printf '%s' "$line" | awk '{print $2}')
    pid=$(printf '%s' "$line" | awk '{print $1}')
    if [ "$pid" != "-" ]; then
      # プロセス稼働中なら健全（status 欄は「前回終了時」の値なので無視。kickstart 直後の -15 等を誤検知しない）
      echo "✅ $label : running (pid=${pid})"
    elif [ "$status" != "0" ]; then
      echo "🚨 $label : ロード済みだが最終 exit=${status} (実行失敗中)"
      fail=1
    else
      echo "✅ $label : loaded (exit=0)"
    fi
  else
    echo "🚨 $label : plist はあるのに未ロード（6/10 型事故の疑い）"
    echo "     復旧: launchctl bootstrap gui/\$(id -u) \"$p\""
    fail=1
  fi
done

# 3) 無効化済みの復活チェック
for p in "$LA_DIR"/*.disabled; do
  [ -e "$p" ] || continue
  base=$(basename "$p")
  base=${base%.plist.disabled}
  if printf '%s\n' "$loaded" | grep -q "$base"; then
    echo "⚠️  $base : .disabled なのにロードされている（意図的に止めたはず）"
    warn=$((warn+1))
  fi
done

# 4) TCC 罠スキャン（launchd から ~/Desktop は読めない）
for p in "$LA_DIR"/*.plist; do
  [ -e "$p" ] || continue
  case "$(basename "$p")" in
    com.google.*|com.microsoft.*|com.valvesoftware.*) continue ;;
  esac
  if grep -q "/Users/[^<]*/Desktop" "$p" 2>/dev/null; then
    echo "⚠️  $(basename "$p") : ~/Desktop 配下を参照（TCC で失敗する恐れ。~/Library/Application Support/ へ移設推奨、6/7 教訓）"
    warn=$((warn+1))
  fi
done

# 5) 期待リスト突合（コメント行 # と空行は無視）
if [ -f "$MANIFEST" ]; then
  while IFS= read -r want; do
    case "$want" in ''|\#*) continue ;; esac
    printf '%s\n' "$loaded" | awk -v l="$want" '$3==l{found=1} END{exit !found}' || {
      echo "🚨 $want : 期待リストにあるが未ロード"
      fail=1
    }
  done < "$MANIFEST"
fi

echo "== 結果: $([ $fail -eq 0 ] && echo "OK ✅" || echo "NG 🚨") （警告 $warn 件）=="
exit $fail
