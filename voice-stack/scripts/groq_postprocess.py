"""
groq_postprocess.py - Groq Llama 70B 音声テキスト後処理 (V1 旧構成)

原典:
- 勝間和代 X 投稿 2026-04-10 09:07 (ID 2042393991279493523, 120 likes)
  > ウィスパーモデルは、NVIDIAのチップで動かして、その後のLLMを
  > Llama70BでGroqにやってもらっています。70Bはさすがに個人では
  > もてないので。Groqの フラグシップモデルなので、早いし安いです。

- 勝間和代 X 投稿 2026-04-16 08:48 (ID 2044563515781042310, 39 likes)
  > GPUが載っていないノートパソコンで、Whisperモデルを使うときには、
  > Groqに送っているのですが、このときに日本語であるということを
  > 明確に指定して、句読点のプロンプトを入れると、かなり正確に句読点を
  > 入れることが分かったので、とりあえずLLM処理を外しても良さそうです。

→ V2 (Scribe) 移行で 4/27 から不要化したが、V1 構成 + GPT 120B 比較用に保持

使い方:
  echo "ええと、これは音声入力の結果なんですけれども句読点ないです" | python groq_postprocess.py
  python groq_postprocess.py --text "テキスト直接指定"
  python groq_postprocess.py --check

要件: pip install groq
環境変数: GROQ_API_KEY
モデル: llama-3.3-70b-versatile (フラグシップ)
"""

import argparse
import os
import sys

try:
    from groq import Groq
except ImportError:
    print("[ERROR] groq SDK 必要: pip install groq")
    sys.exit(1)

API_KEY = os.environ.get("GROQ_API_KEY")
DEFAULT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """あなたは日本語音声認識結果のクリーンアップ担当です。
入力テキストに対して以下を実行してください:

1. 適切な句読点 (、。) を挿入
2. 「えーと」「あの」「うーんと」等のフィラーを除去
3. 同じ単語の繰り返しを 1 回に圧縮
4. 漢字変換ミスを文脈で修正
5. 改行は段落の切れ目のみ

出力は本文のみ。前置き・解説・引用符は不要。
"""


def postprocess(text: str, model: str = DEFAULT_MODEL) -> str:
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY が必要です")
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    return completion.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="勝間 V1 stack: Groq Llama 70B 後処理")
    parser.add_argument("--text", help="入力テキスト (省略時は stdin)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Groq モデル (default: {DEFAULT_MODEL})")
    parser.add_argument("--check", action="store_true", help="API キーと SDK 確認のみ")
    args = parser.parse_args()

    if args.check:
        print(f"[CHECK] GROQ_API_KEY = {'SET' if API_KEY else 'NOT SET'}")
        print(f"[CHECK] Default model = {DEFAULT_MODEL}")
        return

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("[ERROR] 入力テキストが空です", file=sys.stderr)
        sys.exit(1)

    cleaned = postprocess(text, args.model)
    print(cleaned)


if __name__ == "__main__":
    main()
