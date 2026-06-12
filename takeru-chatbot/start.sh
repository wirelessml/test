#!/bin/bash
# AIミニマリストしぶ — ワンコマンド起動
#
# 🚨🚨 2026-06-12 セキュリティ警告: このスクリプトは server.py を 0.0.0.0 で公開し
#   cloudflared トンネルで全世界に晒す。現状の server.py は【無認証】で、外部から:
#     - /chat       → Claude API 課金を無制限に焼ける（レート制限は IP 単位・分散で回避可）
#     - /api/voice  → ElevenLabs 課金エンドポイント（レート制限の前で return＝完全ノーガード）
#     - /api/export, /api/history → 全会話ログ（個人の相談内容）を無認証で吸い出せる
#     - /stats      → ユーザー質問を innerHTML 連結＝保存型 XSS
#   公開実績あり（過去 Tailscale Funnel/trycloudflare）。【再公開する前に必ず】
#   docs/projects/review-chatbot-security-2026-06-12.md の提案 1〜8 を実装すること
#   （最低: 127.0.0.1 バインド＋全 API 認証＋/api/voice 課金ガード＋/stats を textContent 化）。
#   それまでトンネル公開は禁止。ローカル検証は下記を 127.0.0.1 に変えてトンネル行を消して使う。
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
