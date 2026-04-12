#!/usr/bin/env python3
"""AIミニマリストしぶ ライブ配信システム
- カメラ映像 + テキストオーバーレイ + しぶ声読み上げ
- YouTube Live Chat連携（APIキー設定時）
- ローカルテスト可能（手動コメント入力モード）
"""

import subprocess, json, os, sys, time, threading, queue, urllib.request, tempfile

# 設定
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE_ID = 'LIDNtfJHRfi2AFJWPFeV'
VOICE_MODEL = 'eleven_v3'
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
STREAM_KEY = os.environ.get('YOUTUBE_STREAM_KEY', '')
RTMP_URL = f'rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}' if STREAM_KEY else ''

# しぶチャットのシステムプロンプト
SYSTEM_PROMPT = """あなたはミニマリストしぶ（澁谷直人、31歳）です。
福岡在住、テスラで車上生活中。月の生活費5.8万円。
「手ぶらで生きる」著者、YouTube登録者40万人。
口調: タメ口、短い、断定的。「〜だよ」「〜だね」「手放そう」
回答は50文字以内で短く。ライブ配信中なのでテンポよく。"""

# キュー
comment_queue = queue.Queue()
display_queue = queue.Queue()

def generate_voice(text, output_path):
    """ElevenLabsでしぶ声を生成"""
    if not ELEVENLABS_API_KEY:
        print("[voice] APIキー未設定、スキップ")
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
    """Claude CLIでしぶとして回答"""
    try:
        prompt = f"{SYSTEM_PROMPT}\n\n視聴者の質問: {question}\nしぶ:"
        result = subprocess.run(
            ['claude', '--print'],
            input=prompt,
            capture_output=True, text=True, timeout=30
        )
        reply = result.stdout.strip().replace('**', '')
        # 50文字制限
        if len(reply) > 80:
            reply = reply[:77] + '...'
        return reply
    except Exception as e:
        print(f"[reply error] {e}")
        return "ちょっと待って。"

def play_audio(path):
    """音声を再生"""
    try:
        subprocess.run(['afplay', path], timeout=30)
    except:
        pass

def process_comments():
    """コメント処理ワーカー"""
    while True:
        try:
            comment = comment_queue.get(timeout=1)
            if comment is None:
                break

            username = comment.get('user', '視聴者')
            text = comment.get('text', '')
            print(f"\n[コメント] {username}: {text}")

            # 1. 質問をしぶ声で読み上げ
            voice_path = tempfile.mktemp(suffix='.mp3')
            print(f"[声] 質問を読み上げ中...")
            if generate_voice(text, voice_path):
                play_audio(voice_path)
                os.unlink(voice_path)

            # 2. しぶとして回答生成
            print(f"[AI] 回答生成中...")
            reply = generate_reply(text)
            print(f"[しぶ] {reply}")

            # 3. 表示キューに追加
            display_queue.put({
                'user': username,
                'question': text,
                'reply': reply,
                'timestamp': time.strftime('%H:%M:%S')
            })

            # 4. 回答も読み上げ（オプション）
            # reply_path = tempfile.mktemp(suffix='.mp3')
            # if generate_voice(reply, reply_path):
            #     play_audio(reply_path)
            #     os.unlink(reply_path)

        except queue.Empty:
            continue
        except Exception as e:
            print(f"[error] {e}")

def generate_overlay_image(width=1280, height=720):
    """テキストオーバーレイ画像を生成（SVG→PNG）"""
    items = []
    while not display_queue.empty():
        try:
            items.append(display_queue.get_nowait())
        except:
            break

    # 最新5件を保持
    if not hasattr(generate_overlay_image, 'history'):
        generate_overlay_image.history = []
    generate_overlay_image.history.extend(items)
    generate_overlay_image.history = generate_overlay_image.history[-5:]

    return generate_overlay_image.history

def start_local_stream():
    """ローカルプレビュー配信（カメラ映像 + オーバーレイ）"""
    print("\n[配信] ローカルプレビューモード")
    print("[配信] カメラ映像をウィンドウに表示します")

    # ffplayでカメラプレビュー
    cmd = [
        'ffplay', '-f', 'avfoundation', '-framerate', '30',
        '-i', '0', '-window_title', 'AIミニマリストしぶ LIVE'
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return proc
    except Exception as e:
        print(f"[配信エラー] {e}")
        return None

def start_youtube_stream():
    """YouTube RTMP配信"""
    if not STREAM_KEY:
        print("[配信] YOUTUBE_STREAM_KEY未設定。ローカルモードで起動します。")
        return start_local_stream()

    print(f"\n[配信] YouTube Liveに配信開始")
    cmd = [
        'ffmpeg',
        '-f', 'avfoundation', '-framerate', '30', '-video_size', '1280x720',
        '-i', '0:0',  # カメラ:マイク
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-b:v', '2500k', '-maxrate', '2500k', '-bufsize', '5000k',
        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', RTMP_URL
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return proc
    except Exception as e:
        print(f"[配信エラー] {e}")
        return None

def poll_youtube_chat(live_chat_id):
    """YouTube Live Chatをポーリング"""
    if not YOUTUBE_API_KEY or not live_chat_id:
        return

    next_page = ''
    while True:
        try:
            url = f'https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={live_chat_id}&part=snippet,authorDetails&key={YOUTUBE_API_KEY}'
            if next_page:
                url += f'&pageToken={next_page}'

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())

            for item in data.get('items', []):
                snippet = item.get('snippet', {})
                author = item.get('authorDetails', {})
                comment_queue.put({
                    'user': author.get('displayName', ''),
                    'text': snippet.get('displayMessage', '')
                })

            next_page = data.get('nextPageToken', '')
            poll_interval = data.get('pollingIntervalMillis', 5000) / 1000
            time.sleep(poll_interval)
        except Exception as e:
            print(f"[chat poll error] {e}")
            time.sleep(10)

def manual_input():
    """手動コメント入力モード"""
    print("\n" + "="*50)
    print("AIミニマリストしぶ ライブ配信システム")
    print("="*50)
    print("コマンド:")
    print("  テキスト入力 → コメントとして処理")
    print("  /quit → 終了")
    print("  /status → 状態表示")
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
                print(f"  ElevenLabs: {'接続済み' if ELEVENLABS_API_KEY else '未設定'}")
                print(f"  YouTube: {'接続済み' if STREAM_KEY else 'ローカルモード'}")
                print(f"  処理済みコメント: {len(getattr(generate_overlay_image, 'history', []))}")
                continue

            comment_queue.put({'user': 'テスト視聴者', 'text': text})
        except (EOFError, KeyboardInterrupt):
            comment_queue.put(None)
            break

if __name__ == '__main__':
    print("AIミニマリストしぶ ライブ配信システム起動")
    print(f"  ElevenLabs: {'OK' if ELEVENLABS_API_KEY else '未設定'}")
    print(f"  YouTube配信: {'OK' if STREAM_KEY else 'ローカルモード'}")
    print(f"  YouTube Chat: {'OK' if YOUTUBE_API_KEY else '手動入力モード'}")

    # コメント処理スレッド起動
    worker = threading.Thread(target=process_comments, daemon=True)
    worker.start()

    # 配信開始
    stream_proc = None
    if '--stream' in sys.argv:
        stream_proc = start_youtube_stream()

    # YouTube Chat ポーリング or 手動入力
    if YOUTUBE_API_KEY and '--chat-id' in sys.argv:
        idx = sys.argv.index('--chat-id')
        chat_id = sys.argv[idx + 1]
        chat_thread = threading.Thread(target=poll_youtube_chat, args=(chat_id,), daemon=True)
        chat_thread.start()
        print("YouTube Live Chatを監視中... Ctrl+Cで終了")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        manual_input()

    # 終了処理
    if stream_proc:
        stream_proc.terminate()
    print("\n配信終了。")
