# AIミニマリストしぶ チャットサーバー

> Last updated: 2026-04-22

## 概要

しぶ（@minimalist_sibu、澁谷直人、ミニマリスト YouTuber）の人格を再現した Web チャットボット。Claude CLI 経由で動作、API キー不要、Claude Pro プラン範囲内で無料稼働。

## 稼働手順

### サーバー起動
```bash
python3 ~/Desktop/ai-minimalist-shibu/server.py
```
ポート 8787 で HTTP サーバー起動

### 外部公開
```bash
cloudflared tunnel --url http://localhost:8787
```
セッション毎に公開 URL が変わる（固定 URL にしたいなら Cloudflare 認証トンネル設定が必要）

### ナレッジ更新
```bash
python3 ai-minimalist-shibu/src/build-knowledge.py
# → サーバー再起動
```

## 構成

- **メインスクリプト**: `~/Desktop/ai-minimalist-shibu/server.py`（668 行、v1.0 完成版）
- **ナレッジベース**: `~/Desktop/ai-minimalist-shibu/knowledge/`（56 ファイル以上）
- **会話ログ**: `~/Desktop/ai-minimalist-shibu/logs/chat_YYYY-MM-DD.jsonl`

## 機能

- しぶ口調の回答生成
- ナレッジベースからの検索（簡易 RAG）
- 生活費計算シート
- 30 の質問体験モード
- ダーク/ライトモード切替
- 会話統計ダッシュボード
- PWA 対応（ホーム画面追加可能）

## 関連ファイル

- 運用ルール: @docs/rules/operations.md
- 過去の実装履歴: @docs/archive/2026-04/2026-04-10.md（Issue 100 件完了時）
