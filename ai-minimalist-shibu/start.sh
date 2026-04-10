#!/bin/bash
# AIミニマリストしぶ — ワンコマンド起動
DIR="$(cd "$(dirname "$0")" && pwd)"
eval "$(/opt/homebrew/bin/brew shellenv zsh)" 2>/dev/null

# 既存プロセスを停止
pkill -f "server.py" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# ナレッジバンドル再生成
python3 "$DIR/src/build-knowledge.py"

# サーバー起動
cd "$DIR" && nohup python3 server.py > /tmp/shibu-server.log 2>&1 &
echo "しぶサーバー起動 (PID: $!)"

# Tunnel起動
nohup cloudflared tunnel --url http://localhost:8787 > /tmp/shibu-tunnel.log 2>&1 &
echo "Cloudflare Tunnel起動中..."
sleep 5

# Tunnel URL取得・表示
URL=$(grep -o 'https://[^ ]*trycloudflare.com' /tmp/shibu-tunnel.log | head -1)
URL=$(grep -o 'https://[^ ]*trycloudflare.com' /tmp/shibu-tunnel.log | head -1)
# ヘルスチェック
if curl -s http://localhost:8787/health | grep -q "ok"; then
  HEALTH="OK"
else
  HEALTH="NG"
fi

echo ""
echo "========================================="
echo "  AIミニマリストしぶ 稼働中"
echo "  ヘルス: $HEALTH"
if [ -n "$URL" ]; then
  echo "  $URL"
  echo "  統計: ${URL}/stats"
fi
echo "========================================="
