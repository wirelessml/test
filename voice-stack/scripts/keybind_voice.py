"""
keybind_voice.py - 勝間式キーバインド (無変換 = Groq, 左 Alt = SuperWhisper エミュ)

原典: 勝間和代 X 投稿 2026-04-11 13:50 (ID 2042827514092118401, 125 likes)
> ウィスパーモデルで音声入力をしているので、Groqを使ったり、
> Superwhisperを使ったりしていろいろ調整しています。一応、今は無変換
> キーでGroqを呼び出すようになって、左AltでSuperwhisperを呼び出す
> ようになっていて、それぞれの通信環境とかマシンによって使い分けています。

このスクリプトは:
- 無変換キー押下中 → 録音 → Groq Whisper → クリップボードへ
- 離すと自動ペースト + 半角スペーストリム

注意: SuperWhisper 本体は GUI アプリなのでこのスクリプトでは起動できない。
左 Alt 部分は本来 SuperWhisper のホットキーとして SuperWhisper 側で設定する。
このスクリプトでは「無変換 = Groq Whisper」のみ実装する。

要件: pip install keyboard pyperclip sounddevice numpy groq
環境変数: GROQ_API_KEY
管理者権限推奨 (グローバルキーフック)

使い方:
  python keybind_voice.py
  Ctrl+C で停止
"""

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
    from groq import Groq
except ImportError as e:
    print(f"[ERROR] 必須パッケージ未インストール: {e}")
    print("pip install keyboard pyperclip sounddevice numpy groq")
    sys.exit(1)

API_KEY = os.environ.get("GROQ_API_KEY")
SAMPLE_RATE = 16000
WHISPER_MODEL = "whisper-large-v3"
JA_PROMPT = "以下は日本語の音声です。句読点を適切に入れてください。"

HOTKEY_GROQ = "non convert"  # 無変換キー (日本語キーボード)

state = {
    "recording": False,
    "audio": [],
    "stream": None,
}
client = Groq(api_key=API_KEY) if API_KEY else None


def audio_callback(indata, frames, time_info, status):
    if state["recording"]:
        state["audio"].append(indata.copy())


def start_recording():
    if state["recording"]:
        return
    state["recording"] = True
    state["audio"] = []
    state["stream"] = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=audio_callback,
    )
    state["stream"].start()
    print("[REC] 開始 (無変換キー押下中)")


def stop_recording_and_transcribe():
    if not state["recording"]:
        return
    state["recording"] = False
    state["stream"].stop()
    state["stream"].close()
    print("[REC] 停止 → 転写開始…")

    audio = np.concatenate(state["audio"], axis=0) if state["audio"] else np.zeros((0, 1), dtype="int16")
    if len(audio) < SAMPLE_RATE // 2:
        print("[REC] 短すぎるのでスキップ")
        return

    wav_path = Path("temp_recording.wav")
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    try:
        with open(wav_path, "rb") as f:
            result = client.audio.transcriptions.create(
                file=(wav_path.name, f.read()),
                model=WHISPER_MODEL,
                language="ja",
                prompt=JA_PROMPT,
            )
        text = result.text.strip().lstrip(" 　\t")
        pyperclip.copy(text)
        print(f"[OK] {text}")
        time.sleep(0.05)
        keyboard.send("ctrl+v")
    except Exception as e:
        print(f"[ERROR] {e}")


def main():
    if not API_KEY:
        print("[ERROR] GROQ_API_KEY 必要")
        sys.exit(1)

    print(f"[keybind] 起動。{HOTKEY_GROQ} を押下中に録音→離すと転写")
    print("[keybind] Ctrl+C で停止")

    # 押下/離上を分離して登録
    keyboard.on_press_key(HOTKEY_GROQ, lambda _: start_recording(), suppress=False)
    keyboard.on_release_key(HOTKEY_GROQ, lambda _: stop_recording_and_transcribe(), suppress=False)

    try:
        keyboard.wait("ctrl+c")
    except KeyboardInterrupt:
        pass
    print("\n[keybind] 停止")


if __name__ == "__main__":
    main()
