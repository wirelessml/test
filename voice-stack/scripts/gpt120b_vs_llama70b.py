"""
gpt120b_vs_llama70b.py - V3: GPT 120B vs Llama 70B 比較

原典: 勝間和代 X 投稿 2026-04-27 23:19 (ID 2048769123254165721, 37 likes)
> とりあえずScribeがあまりにも優秀なので、Whisperモデルで、これまで
> クレンジングを同じGroqでも70BのLlamaで行っていたのを、GPTの120Bで
> 行ってみることにします。これでどちらの方が優秀か比較します。
> この2つでは大体同じくらいのスピードか、ローカルでGPUを…

→ 勝間が予告した検証を仲さん側で先回り実装。

両モデルに同じ入力を投げて、出力・トークン数・所要時間を並べて表示。

使い方:
  echo "テキスト" | python gpt120b_vs_llama70b.py
  python gpt120b_vs_llama70b.py --text "..."
  python gpt120b_vs_llama70b.py --check

要件: pip install groq
環境変数: GROQ_API_KEY (両モデルとも Groq 経由)
"""

import argparse
import os
import sys
import time
from typing import Tuple

try:
    from groq import Groq
except ImportError:
    print("[ERROR] groq SDK 必要: pip install groq")
    sys.exit(1)

API_KEY = os.environ.get("GROQ_API_KEY")

# Groq で利用可能な GPT-OSS 120B モデル
MODEL_GPT_120B = "openai/gpt-oss-120b"
MODEL_LLAMA_70B = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """あなたは日本語音声認識結果のクリーンアップ担当です。
1. 適切な句読点を挿入
2. フィラー (えーと、あの) を除去
3. 同じ単語の繰り返しを圧縮
4. 漢字変換ミスを修正
出力は本文のみ。
"""


def run_model(client: Groq, model: str, text: str) -> Tuple[str, float, dict]:
    start = time.time()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    elapsed = time.time() - start
    out = completion.choices[0].message.content.strip()
    usage = {
        "prompt_tokens": completion.usage.prompt_tokens,
        "completion_tokens": completion.usage.completion_tokens,
        "total_tokens": completion.usage.total_tokens,
    }
    return out, elapsed, usage


def main():
    parser = argparse.ArgumentParser(description="勝間 V3 比較: GPT 120B vs Llama 70B")
    parser.add_argument("--text", help="入力テキスト (省略時 stdin)")
    parser.add_argument("--check", action="store_true", help="動作確認のみ")
    args = parser.parse_args()

    if args.check:
        print(f"[CHECK] GROQ_API_KEY = {'SET' if API_KEY else 'NOT SET'}")
        print(f"[CHECK] GPT 120B = {MODEL_GPT_120B}")
        print(f"[CHECK] Llama 70B = {MODEL_LLAMA_70B}")
        return

    if not API_KEY:
        print("[ERROR] GROQ_API_KEY 必要", file=sys.stderr)
        sys.exit(1)

    text = args.text if args.text else sys.stdin.read()
    if not text.strip():
        print("[ERROR] 入力テキストが空", file=sys.stderr)
        sys.exit(1)

    client = Groq(api_key=API_KEY)

    print(f"\n=== 入力 ({len(text)} chars) ===\n{text}\n")

    for label, model in [("Llama 70B", MODEL_LLAMA_70B), ("GPT 120B", MODEL_GPT_120B)]:
        try:
            out, elapsed, usage = run_model(client, model, text)
            print(f"--- {label} ({elapsed:.2f}s, {usage['total_tokens']} tokens) ---")
            print(out)
            print()
        except Exception as e:
            print(f"--- {label}: FAILED ---")
            print(f"ERROR: {e}\n")


if __name__ == "__main__":
    main()
