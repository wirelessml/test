"""
scribe_api.py - ElevenLabs Scribe 直叩き音声→テキスト

原典: 勝間和代 X 投稿 2026-04-27 11:46 (ID 2048594516828151961, 1168 likes)
> あんなに苦労してOpenAIのWhisperモデルとLLMの組み合わせを試していたんだけれども、
> Scribeの新しいバージョンの音声認識ソフトが優秀すぎて、LLMいらずで十分に認識して
> くれます。もうこれだけでローカルでいい気がするな。

特長 (4/27 マニフェストより 4 点):
1. ノイズ耐性 (屋外/カフェ向き)
2. 相槌 (うん、はい、なるほど) 認識保持
3. ハルシネーション解消
4. LLM 後処理不要

使い方:
  python scribe_api.py path/to/audio.wav
  python scribe_api.py --record 10  # 10 秒録音して即転写
  python scribe_api.py --watch       # クリップボードに結果も入れる

要件:
  pip install elevenlabs sounddevice numpy pyperclip
  環境変数 ELEVENLABS_API_KEY
"""

import argparse
import io
import os
import sys
import time
import wave
from pathlib import Path

try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    print("[ERROR] elevenlabs SDK 必要: pip install elevenlabs")
    sys.exit(1)

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    print("[WARN] ELEVENLABS_API_KEY 未設定 (動作確認は --check でできます)")

SCRIBE_MODEL_ID = "scribe_v1"  # 4/27 時点の最新


def transcribe(audio_path: Path, language_code: str = "ja") -> str:
    if not API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY が必要です")
    client = ElevenLabs(api_key=API_KEY)
    with open(audio_path, "rb") as f:
        result = client.speech_to_text.convert(
            file=f,
            model_id=SCRIBE_MODEL_ID,
            language_code=language_code,
            tag_audio_events=False,
            diarize=False,
        )
    return result.text if hasattr(result, "text") else str(result)


def record_to_wav(seconds: int, output_path: Path, sample_rate: int = 16000) -> Path:
    try:
        import sounddevice as sd
        import numpy as np
    except ImportError:
        print("[ERROR] 録音には sounddevice + numpy が必要")
        sys.exit(1)
    print(f"[REC] {seconds} 秒録音開始…")
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    print(f"[REC] 完了 -> {output_path}")
    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return output_path


def main():
    parser = argparse.ArgumentParser(description="勝間 V2 stack: Scribe 直叩き")
    parser.add_argument("audio", nargs="?", help="WAV/MP3 ファイルパス")
    parser.add_argument("--record", type=int, metavar="SEC", help="N 秒録音して転写")
    parser.add_argument("--watch", action="store_true", help="結果をクリップボードへ")
    parser.add_argument("--check", action="store_true", help="API キー有無のみ確認")
    parser.add_argument("--lang", default="ja", help="言語コード (default: ja)")
    args = parser.parse_args()

    if args.check:
        print(f"[CHECK] ELEVENLABS_API_KEY = {'SET' if API_KEY else 'NOT SET'}")
        try:
            from elevenlabs.client import ElevenLabs
            print(f"[CHECK] elevenlabs SDK OK")
        except Exception as e:
            print(f"[CHECK] SDK NG: {e}")
        return

    if args.record:
        wav_path = Path("recording.wav")
        record_to_wav(args.record, wav_path)
        text = transcribe(wav_path, args.lang)
    elif args.audio:
        text = transcribe(Path(args.audio), args.lang)
    else:
        parser.print_help()
        return

    print(text)
    if args.watch:
        try:
            import pyperclip
            pyperclip.copy(text)
            print("[CLIP] クリップボードへコピー済", file=sys.stderr)
        except ImportError:
            print("[WARN] pyperclip 未インストール", file=sys.stderr)


if __name__ == "__main__":
    main()
