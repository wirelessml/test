#!/usr/bin/env python3
"""AIミニマリストしぶ ライブ配信システム v2
- 画面キャプチャ + オーバーレイ + しぶ声読み上げ
- YouTube Live Chat自動連携
- ブラウザオーバーレイ（http://localhost:8789）
"""

import subprocess, json, os, sys, time, threading, queue, urllib.request, tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler

import signal
_original_signal = signal.signal
def _safe_signal(signum, handler):
    try:
        return _original_signal(signum, handler)
    except ValueError:
        return None  # スレッドからのsignal呼び出しを無視
signal.signal = _safe_signal

try:
    import pytchat
    HAS_CHAT = True
except ImportError:
    HAS_CHAT = False

# 設定
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE_ID = 'LIDNtfJHRfi2AFJWPFeV'
VOICE_MODEL = 'eleven_v3'
STREAM_KEY = os.environ.get('YOUTUBE_STREAM_KEY', '')
RTMP_URL = f'rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}' if STREAM_KEY else ''
VIDEO_ID = os.environ.get('YOUTUBE_VIDEO_ID', '')
OVERLAY_PORT = 8789

# しぶシステムプロンプト
SYSTEM_PROMPT = """あなたはミニマリストしぶ（澁谷直人、31歳）です。
福岡在住、テスラで車上生活中。月の生活費5.8万円。
「手ぶらで生きる」著者、YouTube登録者40万人。
口調: タメ口、短い、断定的。「〜だよ」「〜だね」「手放そう」
回答は50文字以内で短く。ライブ配信中なのでテンポよく。"""

# 共有データ
comment_queue = queue.Queue()
chat_history = []  # [{user, question, reply, timestamp}, ...]
chat_lock = threading.Lock()

def generate_voice(text, output_path):
    """ElevenLabsでしぶ声を生成"""
    if not ELEVENLABS_API_KEY:
        return False
    try:
        req = urllib.request.Request(
            f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}',
            data=json.dumps({
                'text': text[:678],
                'model_id': VOICE_MODEL,
                'voice_settings': {'stability': 0.5, 'similarity_boost': 1.0, 'style': 0.0}
            }).encode(),
            headers={'xi-api-key': ELEVENLABS_API_KEY, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(output_path, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"[voice error] {e}")
        return False

def generate_reply(question):
    """"""
    import random
    responses = [
        "いいね。",
        "シンプルが一番だよ。",
        "それ、手放そう。",
        "ありがとう。",
        "まさにそうだね。",
        "モノより経験だよ。",
        "いい質問だね。",
        "自分らしく生きよう。",
    ]
    return random.choice(responses)

def play_audio(path):
    """afplayで音声を再生"""
    import shutil
    queue_dir = '/tmp/shibu-voice-queue'
    os.makedirs(queue_dir, exist_ok=True)
    dest = os.path.join(queue_dir, f'{time.time():.3f}.mp3')
    shutil.copy(path, dest)
    try:
        subprocess.run(['/usr/bin/afplay', path], timeout=30)
    except Exception as e:
        print(f"[audio error] {e}")

def process_comments():
    """コメント処理ワーカー"""
    while True:
        try:
            comment = comment_queue.get(timeout=1)
            if comment is None:
                break

            username = comment.get('user', '視聴者')
            text = comment.get('text', '')
            print(f"[コメント] {username}: {text}")

            # コメントを読み上げ
            voice_path = tempfile.mktemp(suffix='.mp3')
            print(f"[声] 読み上げ中...")
            if generate_voice(text, voice_path):
                play_audio(voice_path)
                try: os.unlink(voice_path)
                except: pass

            # 履歴に追加（オーバーレイ用）
            entry = {
                'user': username, 'question': text,
                'reply': '', 'timestamp': time.strftime('%H:%M:%S')
            }
            with chat_lock:
                chat_history.append(entry)
                if len(chat_history) > 10:
                    del chat_history[:-10]

        except queue.Empty:
            continue
        except Exception as e:
            print(f"[error] {e}")


# --- オーバーレイHTTPサーバー ---

OVERLAY_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="3">
<title>しぶ LIVE オーバーレイ</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: transparent;
    font-family: 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
    overflow: hidden;
}
.overlay {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 420px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.card {
    background: rgba(0, 0, 0, 0.82);
    border-radius: 16px;
    padding: 16px 20px;
    color: #fff;
    border-left: 4px solid #00e676;
    animation: slideIn 0.5s ease-out;
}
@keyframes slideIn {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
.card .user {
    font-size: 12px;
    color: #aaa;
    margin-bottom: 4px;
}
.card .user span {
    color: #00e676;
    font-weight: bold;
}
.card .question {
    font-size: 14px;
    color: #ccc;
    margin-bottom: 8px;
    padding-left: 8px;
    border-left: 2px solid #555;
}
.card .reply {
    font-size: 18px;
    font-weight: bold;
    line-height: 1.5;
    color: #fff;
}
.header {
    background: rgba(0, 0, 0, 0.9);
    border-radius: 16px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.header .dot {
    width: 10px; height: 10px;
    background: #f44336;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.header .title {
    color: #fff;
    font-size: 14px;
    font-weight: bold;
}
.header .count {
    color: #aaa;
    font-size: 12px;
    margin-left: auto;
}
.empty {
    background: rgba(0, 0, 0, 0.6);
    border-radius: 16px;
    padding: 40px 20px;
    text-align: center;
    color: #888;
    font-size: 14px;
}
</style>
</head>
<body>
<div class="overlay">
    <div class="header">
        <div class="dot"></div>
        <div class="title">AIミニマリストしぶ LIVE</div>
        <div class="count">%%COUNT%% 件の質問</div>
    </div>
    %%CARDS%%
</div>
</body>
</html>"""

class OverlayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/history':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with chat_lock:
                self.wfile.write(json.dumps(chat_history, ensure_ascii=False).encode())
        elif self.path == '/' or self.path == '/overlay':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with chat_lock:
                cards_html = ''
                for item in chat_history[-5:]:
                    cards_html += f'''<div class="card">
                        <div class="user"><span>{item["user"]}</span> {item["timestamp"]}</div>
                        <div class="question">{item["question"]}</div>
                        <div class="reply">{item["reply"]}</div>
                    </div>\n'''
                if not cards_html:
                    cards_html = '<div class="empty">コメントを待っています...</div>'
                html = OVERLAY_HTML.replace('%%CARDS%%', cards_html)
                html = html.replace('%%COUNT%%', str(len(chat_history)))
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # ログ抑制

def start_overlay_server():
    server = HTTPServer(('0.0.0.0', OVERLAY_PORT), OverlayHandler)
    print(f"[overlay] http://localhost:{OVERLAY_PORT}/overlay")
    server.serve_forever()

# --- YouTube Live Chat (pytchat、APIキー不要) ---

def poll_youtube_chat(video_id):
    if not video_id:
        print("[chat] VIDEO_ID not set")
        return
    if not HAS_CHAT:
        print("[chat error] pytchat not installed")
        return
    print(f"[chat] YouTube Live Chat start (video: {video_id}, pytchat)")
    retry_count = 0
    max_retries = 50
    while retry_count < max_retries:
        try:
            chat = pytchat.create(video_id=video_id)
            print(f"[chat] pytchat connected (alive: {chat.is_alive()})")
            retry_count = 0
            while chat.is_alive():
                for c in chat.get().sync_items():
                    text = c.message
                    username = c.author.name
                    if text:
                        print(f"[chat] @{username}: {text}")
                        comment_queue.put({'user': f'@{username}', 'text': text})
                time.sleep(2)
            print("[chat] pytchat disconnected")
        except Exception as e:
            print(f"[chat error] pytchat: {e}")
        retry_count += 1
        wait = min(10 * retry_count, 60)
        print(f"[chat] {wait}秒後に再接続... (試行 {retry_count}/{max_retries})")
        time.sleep(wait)
    print("[chat] 再接続上限到達、手動入力モードで続行")

# --- 配信 ---

def start_youtube_stream():
    """YouTube RTMP配信（画面キャプチャ）"""
    if not STREAM_KEY:
        print("[配信] YOUTUBE_STREAM_KEY未設定")
        return None

    print(f"[配信] YouTube Liveに画面配信開始")
    cmd = [
        os.path.expanduser('~/local/bin/ffmpeg'),
        '-f', 'avfoundation', '-framerate', '30',
        '-capture_cursor', '1', '-capture_mouse_clicks', '1',
        '-i', '1:0',  # 画面キャプチャ:MacBook Airマイク
        '-vf', 'scale=1280:720',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-b:v', '2500k', '-maxrate', '2500k', '-bufsize', '5000k',
        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', RTMP_URL
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return proc
    except Exception as e:
        print(f"[配信エラー] {e}")
        return None

def manual_input():
    """手動コメント入力モード"""
    print("\n" + "="*50)
    print("AIミニマリストしぶ ライブ配信システム v2")
    print("="*50)
    print("コマンド:")
    print("  テキスト入力 → コメントとして処理")
    print("  /quit   → 終了")
    print("  /status → 状態表示")
    print(f"  オーバーレイ → http://localhost:{OVERLAY_PORT}/overlay")
    print("="*50 + "\n")

    while True:
        try:
            text = input("💬 コメント> ").strip()
            if not text:
                continue
            if text == '/quit':
                comment_queue.put(None)
                break
            if text == '/status':
                with chat_lock:
                    cnt = len(chat_history)
                print(f"  ElevenLabs: {'OK' if ELEVENLABS_API_KEY else '未設定'}")
                print(f"  配信: {'OK' if STREAM_KEY else 'ローカル'}")
                print(f"  Chat: {'pytchat OK' if HAS_CHAT and VIDEO_ID else '手動入力'}")
                print(f"  処理済みコメント: {cnt}")
                continue

            comment_queue.put({'user': 'テスト視聴者', 'text': text})
        except (EOFError, KeyboardInterrupt):
            comment_queue.put(None)
            break

if __name__ == '__main__':
    print("=" * 50)
    print("AIミニマリストしぶ ライブ配信システム v2")
    print("=" * 50)
    print(f"  ElevenLabs: {'OK' if ELEVENLABS_API_KEY else '未設定'}")
    chat_ready = bool(VIDEO_ID)
    print(f"  YouTube配信: {'OK' if STREAM_KEY else 'ローカルモード'}")
    print(f"  YouTube Chat: {'OK (pytchat)' if chat_ready else '手動入力モード'}")
    print(f"  オーバーレイ: http://localhost:{OVERLAY_PORT}/overlay")

    # 1. オーバーレイサーバー起動
    overlay_thread = threading.Thread(target=start_overlay_server, daemon=True)
    overlay_thread.start()

    # 2. コメント処理ワーカー起動
    worker = threading.Thread(target=process_comments, daemon=True)
    worker.start()

    # 3. 配信開始
    stream_proc = None
    if '--stream' in sys.argv:
        stream_proc = start_youtube_stream()

    # 4. YouTube Chat自動連携（pytchat、APIキー不要）
    chat_thread = None
    vid = VIDEO_ID
    if '--video-id' in sys.argv:
        idx = sys.argv.index('--video-id')
        vid = sys.argv[idx + 1]
    if vid:
        chat_thread = threading.Thread(target=poll_youtube_chat, args=(vid,), daemon=True)
        chat_thread.start()

    # 5. 手動入力（Chat連携中も併用可能）
    manual_input()

    # 終了処理
    if stream_proc:
        stream_proc.terminate()
        print("[配信] 停止")
    print("\n配信終了。")
