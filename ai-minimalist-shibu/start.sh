#!/bin/bash
# AIミニマリストしぶ — ワンコマンド起動
DIR="$(cd "$(dirname "$0")" && pwd)"
eval "$(/opt/homebrew/bin/brew shellenv zsh)" 2>/dev/null

# 既存プロセスを停止
pkill -f "server.py" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# サーバー起動
cd "$DIR" && nohup python3 server.py > /tmp/shibu-server.log 2>&1 &
echo "しぶサーバー起動 (PID: $!)"

# Tunnel起動
nohup cloudflared tunnel --url http://localhost:8787 > /tmp/shibu-tunnel.log 2>&1 &
echo "Cloudflare Tunnel起動中..."
sleep 5

# Tunnel URL取得・表示
URL=$(grep -o 'https://[^ ]*trycloudflare.com' /tmp/shibu-tunnel.log | head -1)
if [ -n "$URL" ]; then
  echo ""
  echo "========================================="
  echo "  AIミニマリストしぶ 稼働中"
  echo "  $URL"
  echo "========================================="
else
  echo "Tunnel URL取得待ち... cat /tmp/shibu-tunnel.log で確認"
fi
