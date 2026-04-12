# 会話記録 2026-04-12（夕方・コワーキング）

## 概要

AIミニマリストしぶ ライブ配信システムをYouTube Liveで完全動作させた。YouTube Chat自動取得→しぶ声読み上げ→AI回答→オーバーレイ表示の全フローが成功。

## 環境

- Wi-Fi: YKSmas318（5GHz, 802.11ax）
- Claude Code: Terminal.appで直接起動
- macOS: 26.5.0、M1 8GB

## 実施内容

### 1. 前セッションの確認・引き継ぎ
- conversation_log_20260412_afternoon.md（18項目）を確認
- 最後のコミット: ライブ配信システム プロトタイプ（shibu-live.py v1, 271行）

### 2. shibu-live.py v2 構築
- v1（プロトタイプ）→ v2（全面改修、403行）
- **オーバーレイHTTPサーバー**（localhost:8789）: Q&Aカード表示、CSS animation、3秒自動更新
- **回答もしぶ声で読み上げ**（v1は質問のみ）
- **YouTube Chat自動取得**: chat_downloader → pytchat（signalパッチ）
- **API履歴エンドポイント**: /api/history（JSON）

### 3. YouTube Live配信テスト（試行錯誤）

#### ビットレート問題
- 静的画面キャプチャではx264が超効率圧縮 → 42Kbps（YouTube推奨: 1500Kbps以上）
- 解決: ノイズフィルタ `noise=alls=40:allf=t+u` で1800Kbps確保
- CRF、CBR、VideoToolbox等を試したが、ノイズフィルタが最も効果的

#### ffmpegの最終コマンド
```bash
~/local/bin/ffmpeg \
  -f avfoundation -framerate 30 \
  -capture_cursor 1 -capture_mouse_clicks 1 \
  -i "2:2" \
  -vf "scale=1280:720,noise=alls=40:allf=t+u" \
  -pix_fmt yuv420p \
  -c:v libx264 -preset fast \
  -profile:v high -level:v 4.1 \
  -b:v 2500k -bufsize 1000k \
  -g 60 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv "rtmp://a.rtmp.youtube.com/live2/STREAM_KEY"
```

#### 「動画を再生できません」問題
- YouTube Studioでは「非常に良い」なのに公開ページで再生不可
- 原因1: ffmpegを何度も再接続 → ストリームがエラー状態に
- 原因2: 古いストリームが終了されずストリームキーが紐付いたまま
- 原因3: 子ども向け設定 → チャットが無効化される
- 原因4: 音声ビットレート0 → マイクが無音を送信
- **解決**: 古いストリームを終了 + 子ども向けでない + チャットON + 公開 + ffmpeg1回接続

#### 24時間制限の調査
- 別アカウントで「あと23:59:10でライブ配信が可能になります」を確認
- しかし仲啓輔アカウントは全機能「有効」（標準/中級/上級すべて緑）
- **結論: 24時間制限ではなく、設定・接続の問題だった**

### 4. YouTube Chat自動取得

#### chat_downloader（失敗）
- `pip3 install chat-downloader` (v0.2.8)
- エラー: `Unable to parse initial video data` — ライブラリの互換性問題
- YouTube Live Chatページのスクレイピングも試行 → continuation tokenなし

#### pytchat（成功）
- `pip3 install pytchat` (v0.5.5)
- 問題: スレッド内で `signal only works in main thread` エラー
- **解決**: `signal.signal` をモンキーパッチ（スレッドからの呼び出しをtry/exceptで無視）
- 最終テストで @wirelessml のコメント2件を自動取得成功

### 5. 最終成功テスト

#### 動作確認済みの全フロー
1. ffmpegが画面キャプチャをYouTube LiveにRTMP配信
2. 視聴者がYouTubeチャットにコメント投稿
3. pytchatがコメントを自動取得
4. ElevenLabsでコメントをしぶ声で読み上げ
5. Claude CLI（`--print`）でしぶとして回答生成
6. ElevenLabsで回答をしぶ声で読み上げ
7. オーバーレイ（localhost:8789）にQ&Aカード表示
8. 画面キャプチャでオーバーレイも配信に映る

#### 成功時のログ
```
[chat] @wirelessml: はい
[しぶ] はい、いいね。素直が一番だよ。
[chat] @wirelessml: 聞こえた
[しぶ] 聞こえてるよ、ありがとう。よろしくね。
```

### 6. YouTube配信の教訓

| 問題 | 原因 | 解決策 |
|------|------|--------|
| ビットレート42Kbps | 静的画面のx264超効率圧縮 | ノイズフィルタ(`noise=alls=40`) |
| 動画を再生できません | ffmpeg再接続でストリームエラー | 1回で接続、古いストリーム終了 |
| チャット無効 | 子ども向け設定 | 「子ども向けではない」に変更 |
| 音声ビットレート0 | マイクが無音を送信 | 部屋で音を出す/BGMトーン再生 |
| ストリーミング準備中(永遠) | デュアルストリームON? | デュアルストリームOFF |
| chat_downloader失敗 | ライブラリ互換性 | pytchat + signalパッチに変更 |
| pytchat signal error | スレッド内signal呼び出し | signal.signalをモンキーパッチ |

### 7. YouTubeアカウント情報

| アカウント | ストリームキー | チャンネル | 配信可能 |
|-----------|------------|----------|---------|
| 仲啓輔 | `pg5g-27x1-k8s9-a6um-1srj` | UCHLkN8orefort4C7es8XofPg | OK（全機能有効） |
| ゆいか | `31ph-0za2-ce26-my5j-bxga` | UCxRflDAV9QVV2N7Gfo9ONg | OK |

### 8. Git コミット

- `03d62ab` shibu-live.py v2: オーバーレイ・YouTube Chat・回答読み上げ追加
- `117b007` CLAUDE.md: ライブ配信システムv2構築・YouTube 24時間制限を記録
- `9ddfe55` shibu-live.py v2.1: YouTube Chat自動取得成功（pytchat + signalパッチ）

## システム状態（セッション終了時）

- 稼働時間: 7時間25分+
- Load Average: 1.76
- メモリ空き: 61%
- Claude CLI: 797MB
- ffmpeg: 停止
- YouTube Live: 配信終了

## インストール済みパッケージ（本セッション）

- pytchat 0.5.5
- chat-downloader 0.2.8
- httpx 0.28.1, h2 4.3.0, anyio 4.12.1 等（pytchat依存）

## 次回やること

- ライブ配信の本番運用テスト（長時間安定性）
- オーバーレイのデザイン改善（配信画面に合わせたレイアウト）
- ElevenLabsクレジット残量確認（残約35,000）
- 配信起動をワンコマンド化（start-live.sh）
