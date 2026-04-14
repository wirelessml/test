#!/bin/bash
# 定時報告スクリプト
cd /Users/yuika/Desktop

# 1. スクリーンショット（GUI接続時のみ）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCREENSHOT="screenshots/remote_${TIMESTAMP}.png"
mkdir -p screenshots
if screencapture -x -D 1 "$SCREENSHOT" 2>/dev/null; then
    HAS_SCREENSHOT=true
else
    SCREENSHOT="(unavailable from SSH/cron)"
    HAS_SCREENSHOT=false
fi

# 2. ネットワーク情報
SSID=$(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I 2>/dev/null | awk '/ SSID/ {print $2}')
IP=$(ipconfig getifaddr en0 2>/dev/null || echo "unknown")

# 3. サービス状態
SHIBU_CHAT=$(screen -ls 2>/dev/null | grep -q shibu-chat && echo "running" || echo "stopped")
OBS_STATUS=$(pgrep -x OBS >/dev/null && echo "running" || echo "stopped")
LOAD=$(sysctl -n vm.loadavg 2>/dev/null | tr -d '{}')

# 4. log.json更新
NOW=$(date +%Y-%m-%dT%H:%M:%S+09:00)
TODAY=$(date +%Y-%m-%d)
python3 -c "
import json
d = {
    'last_updated': '$NOW',
    'session': '$TODAY',
    'status': 'active',
    'screenshot': '$SCREENSHOT',
    'network': {'type': 'Wi-Fi', 'ssid': '$SSID', 'ip': '$IP'},
    'services': {'shibu_chat': '$SHIBU_CHAT', 'obs': '$OBS_STATUS', 'load': '$LOAD'}
}
with open('log.json', 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
"

# 5. git commit & push
git add log.json 2>/dev/null
if [ "$HAS_SCREENSHOT" = true ]; then
    git add "$SCREENSHOT" 2>/dev/null
fi
git commit -m "リモートコントロール状態報告 $(date '+%Y/%m/%d %H:%M') - 定時報告" 2>/dev/null
git push origin main 2>/dev/null
