"""
keybind_scribe.py - 無変換キー = ElevenLabs Scribe push-to-talk (V4 完全自前版)

V4 設計: SuperWhisper Free 枠で Scribe 使えないので、Python で直接 Scribe API を叩く。
勝間 4/27 朝の構成「Scribe pure stack」を SuperWhisper 経由ではなく自前で再現。

ホットキー選定理由:
- 無変換キー（Japanese keyboard）= 単独で他機能と干渉しない、ergonomically space bar 隣
- 左 Alt は Alt+Tab / Alt+F4 / メニューアクセスと干渉、push-to-talk に不向き
- 勝間 4/11 13:50 の「無変換 = Groq」を踏襲、Scribe に置換

フロー:
  1. 無変換キー押下 → 録音開始
  2. 無変換キー離す → 録音終了 → Scribe API → テキスト取得
  3. 先頭/末尾の空白を Python トリム（勝間 4/15 Python トリム再現）
  4. 漢数字 → 算用数字 ローカル正規表現補正
  5. クリップボードに格納 + 自動ペースト (Ctrl+V)

要件:
  pip install keyboard pyperclip sounddevice numpy elevenlabs
環境変数:
  ELEVENLABS_API_KEY (必須)

使い方:
  python keybind_scribe.py
  → 無変換キー長押し → 発話 → 離す → カーソル位置に貼付け
  Ctrl+C で停止
"""

import io
import os
import sys
import threading
import time
import wave
from pathlib import Path

try:
    import keyboard
    import pyperclip
    import sounddevice as sd
    import numpy as np
    from elevenlabs.client import ElevenLabs
except ImportError as e:
    print(f"[ERROR] 必須パッケージ未インストール: {e}")
    print("pip install keyboard pyperclip sounddevice numpy elevenlabs")
    sys.exit(1)

# ローカル正規表現の漢数字 → 算用数字補正をインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from scribe_kanjisuji_local import convert as kanjisuji_convert
    KANJI_FIX_AVAILABLE = True
except ImportError:
    print("[WARN] scribe_kanjisuji_local.py が見つかりません。漢数字補正なしで動作します")
    KANJI_FIX_AVAILABLE = False

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    print("[ERROR] ELEVENLABS_API_KEY 未設定")
    print("PowerShell で: setx ELEVENLABS_API_KEY \"sk_...\"")
    sys.exit(1)

SAMPLE_RATE = 16000
SCRIBE_MODEL_ID = "scribe_v1"
HOTKEY = "non convert"  # 無変換キー (Japanese keyboard)
LANGUAGE = "ja"

# 録音状態
recording = False
audio_frames = []
record_lock = threading.Lock()
client = ElevenLabs(api_key=API_KEY)


def trim_text(text: str) -> str:
    """先頭・末尾の空白を除去（勝間 4/15 Python トリム再現）"""
    if not text:
        return text
    text = text.lstrip(" 　\t\r\n")
    text = text.rstrip(" 　\t\r\n")
    return text


def audio_callback(indata, frames, time_info, status):
    """sounddevice からの音声フレームをバッファに蓄積"""
    if recording:
        audio_frames.append(indata.copy())


def transcribe(audio_data: np.ndarray) -> str:
    """ElevenLabs Scribe API で音声をテキスト化"""
    # NumPy → WAV (in memory)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    buf.seek(0)
    buf.name = "audio.wav"

    result = client.speech_to_text.convert(
        file=buf,
        model_id=SCRIBE_MODEL_ID,
        language_code=LANGUAGE,
        tag_audio_events=False,
        diarize=False,
    )
    return result.text if hasattr(result, "text") else str(result)


def on_press():
    """無変換キー押下 → 録音開始"""
    global recording, audio_frames
    with record_lock:
        if recording:
            return
        audio_frames = []
        recording = True
    print(f"[REC] 録音開始")


def on_release():
    """無変換キー離す → 録音終了 → Scribe → クリップボード"""
    global recording, audio_frames
    with record_lock:
        if not recording:
            return
        recording = False
        frames_copy = audio_frames[:]

    if not frames_copy:
        print(f"[WARN] 音声フレームなし")
        return

    # フレームを連結
    audio_data = np.concatenate(frames_copy, axis=0).flatten()
    duration = len(audio_data) / SAMPLE_RATE
    print(f"[REC] 録音終了 ({duration:.1f}s) → Scribe 転写中...")

    if duration < 0.3:
        print("[WARN] 録音時間が短すぎます (0.3s 未満)、スキップ")
        return

    try:
        t0 = time.time()
        text = transcribe(audio_data)
        elapsed = time.time() - t0
    except Exception as e:
        print(f"[ERROR] Scribe API 失敗: {e}")
        return

    text = trim_text(text)
    if not text:
        print("[WARN] 転写結果が空")
        return

    if KANJI_FIX_AVAILABLE:
        before = text
        text = kanjisuji_convert(text)
        if before != text:
            print(f"[漢数字補正] {before[:30]} → {text[:30]}")

    pyperclip.copy(text)
    print(f"[OK] {elapsed:.1f}s, {len(text)}c: {text[:60]}")

    # 自動ペースト
    time.sleep(0.05)
    keyboard.send("ctrl+v")


def main():
    print("=== keybind_scribe (V4 完全自前版) ===")
    print(f"API Key: {API_KEY[:8]}...")
    print(f"Hotkey: {HOTKEY} (押下中録音、離して転写)")
    print(f"Model: {SCRIBE_MODEL_ID}")
    print(f"Language: {LANGUAGE}")
    print(f"漢数字補正: {'ON' if KANJI_FIX_AVAILABLE else 'OFF'}")
    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print("Ctrl+C で停止\n")

    keyboard.on_press_key(HOTKEY, lambda _: on_press(), suppress=False)
    keyboard.on_release_key(HOTKEY, lambda _: on_release(), suppress=False)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
    ):
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n[STOP] 終了")


if __name__ == "__main__":
    main()
