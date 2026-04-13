# OBS YouTube Live セッションログ 2026-04-13

## 概要
YouTubeライブ配信中にコメント読み上げが動作しない問題を修正。

## 発生していた問題
1. **動画IDが無効** - `ARsfrFWGm78` (存在しないID) がセットされていた
2. **pytchat 0.5.5がメッセージを取得できない** - 接続はaliveだがメッセージが空
3. **音声が再生されない** - `play_audio`にafplayが無く、ファイルコピーのみだった
4. **Claude CLI未ログイン** - AI回答が「Not logged in」になっていた

## 修正内容

### 1. 動画ID修正
- 無効な `ARsfrFWGm78` → 正しい `mRE18XYo6rg` に更新
- YouTube Data APIで `liveStreamingDetails.activeLiveChatId` を確認

### 2. チャット取得方式の変更 (pytchat → YouTube Data API)
- pytchat 0.5.5 が動作不良のため、YouTube Data API `liveChat/messages` エンドポイントに切り替え
- `get_live_chat_id()` で動画IDからliveChatIdを取得
- `poll_youtube_chat()` でpollingIntervalMillisに従いポーリング
- APIキー: YouTube Data API v3

### 3. 音声再生の修正
- `play_audio()` に `/usr/bin/afplay` を追加
- Mac のデフォルト出力デバイス (BlackHole 2ch) 経由で再生
- OBS WebSocket (port 4455) で「BlackHole Audio」入力ソースを追加
- BlackHole 2ch → OBS → YouTube配信 の音声ルーティング確立

### 4. コメント読み上げ専用モード
- AI回答生成 (Claude CLI) を除去し、コメント読み上げのみに簡略化
- `process_comments()` からAI応答・応答音声生成を削除
- ElevenLabsでコメントテキストをTTS → afplayで再生

## 環境
- Mac: yuika.local (M1, macOS 26.5.0)
- OBS: 32.1.1 (プロファイル: YouTube Live)
- Python: 3.9
- 音声: ElevenLabs v3 (Voice ID: LIDNtfJHRfi2AFJWPFeV)
- 音声ルーティング: afplay → BlackHole 2ch → OBS coreaudio_input_capture

## 成果物

### マニュアル作成
- `youtube-live-manual.md` - YouTubeライブ配信+コメント読み上げの運用マニュアル
- Windows PC(操作側) → SSH → Mac(配信側) の役割分担を明記
- 配信開始〜終了の全手順、トラブルシューティング、SSH接続テンプレートを網羅

### claude-mem インストール（両マシン）
- Windows PC: `npx claude-mem install`
  - GitHubのSSH host key問題 → `ssh-keyscan` で解決
  - HTTPS clone失敗 → 手動clone後に再インストールで成功
  - プラグインDir: `C:\Users\gci_admin\.claude\plugins\marketplaces\thedotmack`
- Mac: SSH経由で `npx claude-mem install` → 一発成功
  - プラグインDir: `/Users/yuika/.claude/plugins/marketplaces/thedotmack`

### Mac定時報告の再開
- `report.sh` 作成（スクリーンショット + log.json + git push）
- Mac cron設定: 毎時33分に自動実行 (`33 * * * * /bin/bash report.sh`)
- SSH経由ではscreencaptureが使えないため、スクリーンショットはGUI時のみ取得
- テスト実行成功: `e8e34fc` リモートコントロール状態報告 2026/04/13 13:20
- Gmail下書き作成はbash cronからは不可 → Windows PC側のClaude CodeセッションからCronCreate（毎時33分）で自動実行に変更
  - SSH → Mac状態確認 → log.json更新 → git push → Gmail MCP下書き作成
  - セッション限定（終了で消える、7日で自動期限切れ）

### Claude Code settings.json 最適化（両マシン）
- 以下の環境変数を両マシンの `~/.claude/settings.json` に追加:
  - `CLAUDE_CODE_DISABLE_1M_CONTEXT`: 1Mコンテキスト無効化
  - `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`: 適応的思考無効化
  - `CLAUDE_CODE_DISABLE_AUTO_MEMORY`: 自動メモリ無効化
  - `CLAUDE_CODE_SUBAGENT_MODEL`: サブエージェントをSonnetに

### Mac Claude Code ログイン（認証情報転送）
- Mac側のClaude Code v2.1.104が「Not logged in」状態だった
- iPhone SSHからの `/login` → OAuth URL生成 → Windows PCブラウザで開く方式を試行
  - `start` コマンドでURL中の `&` が壊れ「無効なOAuth要求」エラー
  - `python webbrowser.open()` で再試行するもstate期限切れ
- 最終解決: Windows PCの `~/.claude/.credentials.json` をparamikoでMacにSFTP転送
  - claudeAiOauth（accessToken, refreshToken, subscriptionType: max）をコピー
  - Claude Code再起動 → 「Claude Max」でログイン成功
- Remote Control有効化: `https://claude.ai/code/session_01YWK6zUHC3Ru7PDuahTyUtj`

## コミット
- `ee7dfc8` shibu-live: pytchat→YouTube Data API, afplay音声再生, コメント読み上げ専用モード
- `4ba1e70` Add OBS YouTube Live session log 2026-04-13
- `d15d6a7` Add YouTube Live + comment TTS manual
- `988aaf9` Update manual: Win操作→Mac配信の役割分担を明記
- `e8e34fc` リモートコントロール状態報告 2026/04/13 13:20 - 定時報告
