"""
groq_whisper.py - Groq Whisper API による音声認識 (V1: GPU なし PC 向け)

原典: 勝間和代 X 投稿 2026-04-10 17:50 (ID 2042525706761207822, 30 likes)
> 特に非力なパソコンの時にウィスパーモデルをGroqに任せることができると
> 随分楽になりました。

勝間 X 投稿 2026-04-16 08:48 (ID 2044563515781042310)
> GPUが載っていないノートパソコンで、Whisperモデルを使うときには、
> Groqに送っているのですが、このときに日本語であるということを明確に
> 指定して、句読点のプロンプトを入れると、かなり正確に句読点を入れる
> ことが分かったので、とりあえずLLM処理を外しても良さそうです。

Groq の whisper-large-v3 エンドポイントを叩く。GPU 不要。

使い方:
  python groq_whisper.py audio.wav
  python groq_whisper.py --record 10
  python groq_whisper.py --check

要件: pip install groq sounddevice numpy
環境変数: GROQ_API_KEY
"""

import argparse
import os
import sys
import wave
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    print("[ERROR] groq SDK 必要: pip install groq")
    sys.exit(1)

API_KEY = os.environ.get("GROQ_API_KEY")
WHISPER_MODEL = "whisper-large-v3"

# 4/16 勝間ツイートの「日本語であることと句読点」プロンプトを忠実再現
JA_PROMPT = "以下は日本語の音声です。句読点を適切に入れてください。"


def transcribe(audio_path: Path, language: str = "ja") -> str:
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY が必要です")
    client = Groq(api_key=API_KEY)
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=(audio_path.name, f.read()),
            model=WHISPER_MODEL,
            language=language,
            prompt=JA_PROMPT,
            response_format="verbose_json",
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
    parser = argparse.ArgumentParser(description="勝間 V1 stack: Groq Whisper API (GPU 不要)")
    parser.add_argument("audio", nargs="?", help="WAV/MP3 ファイル")
    parser.add_argument("--record", type=int, metavar="SEC", help="N 秒録音→転写")
    parser.add_argument("--check", action="store_true", help="動作確認のみ")
    parser.add_argument("--lang", default="ja", help="言語 (default: ja)")
    args = parser.parse_args()

    if args.check:
        print(f"[CHECK] GROQ_API_KEY = {'SET' if API_KEY else 'NOT SET'}")
        print(f"[CHECK] Whisper model = {WHISPER_MODEL}")
        print(f"[CHECK] Prompt = {JA_PROMPT}")
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


if __name__ == "__main__":
    main()
