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

## コミット
- `ee7dfc8` shibu-live: pytchat→YouTube Data API, afplay音声再生, コメント読み上げ専用モード
