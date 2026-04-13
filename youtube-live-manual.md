# YouTubeライブ配信 + コメント読み上げ マニュアル

## 構成

```
Windows PC (MASU-P55 / 100.125.21.47) ← 操作側
│  Claude Code + paramiko で Mac を SSH リモート操作
│  YouTube Studio での配信作成・動画ID確認もここで行う
│
└─→ SSH (Tailscale) ─→ Mac (yuika.local / 100.99.41.2) ← 配信側
                        ├── OBS 32.1.1 → YouTube RTMP配信
                        ├── shibu-live.py → コメント取得 + ElevenLabs TTS + afplay再生
                        └── BlackHole 2ch → OBS音声入力 → 配信に音声を乗せる
```

**ポイント**: Macが配信の実行主体（OBS・音声再生・スクリプト実行）だが、
すべての操作はWindows PCからSSH経由で行う。Mac側でのGUI操作は基本不要。

## 事前準備（初回のみ）

### Windows PC側（操作端末）
- Python + paramiko インストール済み（`pip install paramiko`）
- Tailscale接続済み（Mac: 100.99.41.2）
- SSH接続情報: ユーザー `yuika` / パスワード `naka` / ポート 22
- **注意**: Windows の `python3` は動かない場合あり、`python` を使う

### Mac側（配信端末）
- OBS インストール済み（プロファイル: YouTube Live）
- BlackHole 2ch インストール済み
- ElevenLabs API key が `~/.zshrc` に設定済み
  ```
  export ELEVENLABS_API_KEY=sk_xxxxx
  ```
- Macのデフォルト出力デバイス → BlackHole 2ch（システム設定 > サウンド）
- screen コマンド利用可能

### OBS設定（Mac側、初回のみ）
- 配信先: `rtmp://a.rtmp.youtube.com/live2`
- ストリームキー: YouTube Studioで取得したものを設定
- 音声入力ソース: 「BlackHole Audio」(coreaudio_input_capture, device: BlackHole2ch_UID)
- WebSocket: ポート4455（パスワード設定済み）

---

## 配信手順

**全てWindows PCから実行する。**

### 1. YouTube Studioで配信を作成（Windows PC ブラウザ）
1. https://studio.youtube.com → ライブ配信 → 配信の管理
2. 「配信をスケジュール」or「今すぐ配信」
3. **動画IDをコピー**（URLの `watch?v=` の後ろ11文字、例: `mRE18XYo6rg`）

### 2. OBSで配信開始（Windows PC → Mac SSH）

OBSはMac起動時に自動起動、または事前にGUI操作で起動しておく。
配信開始はOBS WebSocket経由でリモート実行可能:

```bash
# Windows PCから実行: OBS配信開始
PYTHONIOENCODING=utf-8 python -c "
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('100.99.41.2', port=22, username='yuika', password='naka',
            timeout=15, allow_agent=False, look_for_keys=False, banner_timeout=15)
stdin, stdout, stderr = ssh.exec_command('''python3 << 'PY'
import json, websocket, hashlib, base64
ws = websocket.create_connection(\"ws://127.0.0.1:4455\")
hello = json.loads(ws.recv())
auth = hello[\"d\"][\"authentication\"]
secret = base64.b64encode(hashlib.sha256((\"1ChvUoBXUBgZJ1u9\" + auth[\"salt\"]).encode()).digest()).decode()
auth_str = base64.b64encode(hashlib.sha256((secret + auth[\"challenge\"]).encode()).digest()).decode()
ws.send(json.dumps({\"op\": 1, \"d\": {\"rpcVersion\": 1, \"authentication\": auth_str}}))
json.loads(ws.recv())
ws.send(json.dumps({\"op\": 6, \"d\": {\"requestType\": \"StartStream\", \"requestId\": \"1\"}}))
print(json.loads(ws.recv()))
ws.close()
PY
''')
print(stdout.read().decode('utf-8'))
ssh.close()
"
```

### 3. コメント読み上げスクリプト起動（Windows PC → Mac SSH）

```bash
# Windows PCから実行
PYTHONIOENCODING=utf-8 python -c "
import paramiko, time
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('100.99.41.2', port=22, username='yuika', password='naka',
            timeout=15, allow_agent=False, look_for_keys=False, banner_timeout=15)
ssh.exec_command('screen -dmS shibu-chat bash -c \"source ~/.zshrc; export YOUTUBE_VIDEO_ID=<動画ID>; export PYTHONUNBUFFERED=1; cd /Users/yuika/Desktop; python3 -u shibu-live.py 2>&1 | tee /tmp/shibu-chat.log\"')
time.sleep(5)
stdin, stdout, stderr = ssh.exec_command('tail -20 /tmp/shibu-chat.log')
print(stdout.read().decode('utf-8'))
ssh.close()
"
```

`<動画ID>` を手順1で取得したIDに置き換える。

### 4. 動作確認（Windows PCから）

ログに以下が表示されればOK:
```
YouTube Chat: OK (YouTube API)
[chat] liveChatId OK
```

テストコメントを送って、以下のフローを確認:
```
[chat] @ユーザー名: コメント内容
[コメント] @ユーザー名: コメント内容
[声] 読み上げ中...
```

ログ確認コマンド（Windows PCから）:
```bash
PYTHONIOENCODING=utf-8 python -c "
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('100.99.41.2', port=22, username='yuika', password='naka',
            timeout=15, allow_agent=False, look_for_keys=False, banner_timeout=15)
stdin, stdout, stderr = ssh.exec_command('tail -30 /tmp/shibu-chat.log')
print(stdout.read().decode('utf-8'))
ssh.close()
"
```

---

## トラブルシューティング

全てWindows PCからSSH経由で実行する。

### `Cannot find channel id for video id` / メッセージ取得なし
- **原因**: 動画IDが間違っている、またはライブが開始されていない
- **対処**: YouTube Studioで正しい動画IDを確認し、screenセッションを再起動

### `liveChatId` が取得できない
- **原因**: 配信がまだライブ状態になっていない
- **対処**: OBSで配信開始 → YouTube Studio上で「ライブ配信を開始」を実行してから再起動

### 音声が配信に乗らない
- **確認項目**（全てWindows PCからSSH実行）:
  1. Macのデフォルト出力デバイス → BlackHole 2ch か確認
     ```
     system_profiler SPAudioDataType | grep -A2 "Default Output"
     ```
  2. OBSに「BlackHole Audio」入力ソースがあるか確認（OBS WebSocket経由で確認可能）
  3. Macの音量がミュートでないか確認
     ```
     osascript -e "output volume of (get volume settings)"
     osascript -e "output muted of (get volume settings)"
     ```

### screenセッションの再起動（Mac上で実行、SSH経由）
```bash
# 停止
screen -X -S shibu-chat quit

# 起動（動画IDを指定）
screen -dmS shibu-chat bash -c "source ~/.zshrc; export YOUTUBE_VIDEO_ID=<動画ID>; export PYTHONUNBUFFERED=1; cd /Users/yuika/Desktop; python3 -u shibu-live.py 2>&1 | tee /tmp/shibu-chat.log"
```

### ログ確認（Mac上で実行、SSH経由）
```bash
tail -f /tmp/shibu-chat.log
```

---

## 配信終了

全てWindows PCから実行:

1. screenセッション停止（SSH経由）: `screen -X -S shibu-chat quit`
2. OBS配信停止（OBS WebSocket経由、StartStreamをStopStreamに変更）
3. YouTube Studioで配信を終了（Windowsブラウザ）

---

## マシン役割一覧

| マシン | 役割 | 接続 |
|--------|------|------|
| Windows PC (MASU-P55) | 操作・管理（SSH発行元、ブラウザ操作） | ローカル |
| Mac (yuika.local) | 配信実行（OBS、スクリプト、音声再生） | Tailscale SSH 100.99.41.2 |

## ファイル構成

| ファイル | 場所（Mac） | 説明 |
|---------|------------|------|
| shibu-live.py | /Users/yuika/Desktop/ | メインスクリプト |
| /tmp/shibu-chat.log | /tmp/ | 実行ログ |
| /tmp/shibu-voice-queue/ | /tmp/ | 生成された音声ファイル |

## SSH接続テンプレート（Windows PCから）

```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('100.99.41.2', port=22, username='yuika', password='naka',
            timeout=15, allow_agent=False, look_for_keys=False, banner_timeout=15)
# ここにコマンド実行
stdin, stdout, stderr = ssh.exec_command('コマンド')
print(stdout.read().decode('utf-8'))
ssh.close()
```

**注意**: Windows では `python3` ではなく `python` を使う。`PYTHONIOENCODING=utf-8` を付けないと日本語が文字化けする。

## 使用API

| API | 用途 | キー設定 |
|-----|------|---------|
| YouTube Data API v3 | ライブチャット取得 | スクリプト内に埋め込み |
| ElevenLabs v3 | TTS音声生成 | Mac環境変数 `ELEVENLABS_API_KEY` |

## OBS WebSocket (補助)

ポート4455で利用可能。配信開始/停止、BlackHole Audio入力ソースの追加などをWindows PCからリモート実行できる。
パスワードは `/Users/yuika/Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json` に記載。
