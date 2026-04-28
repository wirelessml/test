"""
scribe_kanjisuji_fix.py - Scribe pure stack 専用「漢数字 → 算用数字」補正

原典: 勝間和代 X 投稿群 2026-04-28
- 01:56 (ID 2048944369282191711, 20L)
  > Scribeの最大の欠点の一つが、過剰な正規化で数字を全部漢数字に直したがるので、
  > その部分については後処理でLLMで補正するようにした方が良い気がする
- 06:44 (ID 2049016868237918681, 6L)
  > その辺だけちょっと直す軽いLLMのプロンプトを使ってGroqで直してます
- 13:21 (ID 2049116752504820147, 13L)
  > Scribeやたらと漢数字にしてしまうので、そこだけLLMで直してます
- 20:30 (ID 2049224859465740328, 3L)
  > Scribeが何がすごいかというと、この辺を全部ぶっ飛ばしても、単体で相当高い精度で
  > 日本語をテキスト化してくれる … 前処理や後処理がほとんど不要

V3 比較結論 (4/28 01:15, ID 2048933979420790843, 79L):
> Scribe単体が、Whisperモデル+120BのLLMクレンジングよりも優秀。
> Scribeはハルシネーションせず、足したり消したりしない。

→ よって LLM 後処理は **漢数字補正のみ** の超軽量プロンプトに限定。
   全文クレンジング (groq_postprocess.py) は廃止運用。

使い方:
  echo "二千二十六年四月二十九日の午前六時三十分" | python scribe_kanjisuji_fix.py
  → 2026年4月29日の午前6時30分

  python scribe_kanjisuji_fix.py --text "百二十Bの大規模言語モデル"
  → 120Bの大規模言語モデル

  python scribe_kanjisuji_fix.py --check     # API キー確認のみ
  python scribe_kanjisuji_fix.py --model gpt-oss-120b  # 別モデル指定

要件: pip install groq
環境変数: GROQ_API_KEY
モデル既定: llama-3.1-8b-instant (軽量・高速、漢数字変換に十分)
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

# 軽量モデル既定 - 漢数字 → 算用数字は単純タスクなので 8B で十分高速
DEFAULT_MODEL = "llama-3.1-8b-instant"

# 勝間 4/28 06:44「軽いLLMのプロンプト」相当の最小プロンプト
SYSTEM_PROMPT = """あなたは日本語テキストの漢数字を算用数字に直す専門エディタです。

ルール:
1. 漢数字（一二三四五六七八九十百千万億兆 / 〇零）を算用数字 (0-9) に変換
2. 「年・月・日・時・分・秒・円・人・回・本・個・歳・度・%・GB・TB・B・MB」等の単位の前にある漢数字を変換
3. 慣用句・固有名詞・成語の漢数字は変換しない (例: 一期一会、四国、七五三、千葉、八百屋)
4. 「一つ・二つ・三つ」等の和語数詞は変換しない
5. 出力は変換後の本文のみ、前置きや解説や引用符は一切なし
6. 入力にない単語を加えない、入力にある単語を削らない (Scribeの精度を尊重)

例:
入力: 二千二十六年四月二十九日の午前六時三十分
出力: 2026年4月29日の午前6時30分

入力: 百二十BのLLMで七十Bと比較した
出力: 120BのLLMで70Bと比較した

入力: 一期一会で四国を一周した
出力: 一期一会で四国を一周した
"""


def fix_kanjisuji(text: str, model: str = DEFAULT_MODEL) -> str:
    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY が必要です")
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
        max_tokens=len(text) * 2 + 200,
    )
    return completion.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="勝間 V3 stack: Scribe 漢数字 → 算用数字 軽量補正",
    )
    parser.add_argument("--text", help="入力テキスト (省略時は stdin)")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Groq モデル (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--check", action="store_true", help="API キーと SDK 確認のみ"
    )
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="クリップボード内容を補正してクリップボードに戻す",
    )
    args = parser.parse_args()

    if args.check:
        print(f"[CHECK] GROQ_API_KEY = {'SET' if API_KEY else 'NOT SET'}")
        print(f"[CHECK] Default model = {DEFAULT_MODEL}")
        return

    if args.clipboard:
        try:
            import pyperclip
        except ImportError:
            print("[ERROR] pyperclip が必要: pip install pyperclip")
            sys.exit(1)
        text = pyperclip.paste()
        if not text.strip():
            print("[ERROR] クリップボードが空です", file=sys.stderr)
            sys.exit(1)
        fixed = fix_kanjisuji(text, args.model)
        pyperclip.copy(fixed)
        print(f"[OK] {len(text)}c -> {len(fixed)}c (クリップボード更新済)")
        print(f"[BEFORE] {text[:100]}")
        print(f"[AFTER]  {fixed[:100]}")
        return

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("[ERROR] 入力テキストが空です", file=sys.stderr)
        sys.exit(1)

    fixed = fix_kanjisuji(text, args.model)
    print(fixed)


if __name__ == "__main__":
    main()
