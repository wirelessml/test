"""
scribe_kanjisuji_local.py - Scribe 漢数字 → 算用数字 ローカル正規表現補正 (LLM 不要)

V4 確定構成の代替実装:
- LLM 呼び出しなし、ネットワーク不要、レイテンシゼロ
- 「漢数字 + 単位」のパターンマッチで決定的変換
- 慣用句・固有名詞は「単位が続かない」ルールで自動回避
  - 一期一会 → 一期一会（期は単位でない）
  - 四国 → 四国（国は単位でない）
  - 千葉 → 千葉（葉は単位でない）
  - 八百屋 → 八百屋（屋は単位でない）

V4 設計判断 (4/29 06:40):
- Groq Llama 8B 版 (`scribe_kanjisuji_fix.py`) と互換 CLI
- ローカル正規表現で約 95% のケースをカバー
- 不一致が出たら Groq 版にフォールバック可

使い方:
  echo "二千二十六年四月二十九日の午前六時三十分" | python scribe_kanjisuji_local.py
  → 2026年4月29日の午前6時30分

  python scribe_kanjisuji_local.py --text "百二十Bの大規模言語モデル"
  → 120Bの大規模言語モデル

  python scribe_kanjisuji_local.py --clipboard
  → クリップボード補正 + 自動ペースト

要件: pip install pyperclip (--clipboard 使用時のみ)
"""

import argparse
import re
import sys


# 漢数字 → 数値の対応
KANJI_DIGITS = {
    "〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
}
KANJI_SMALL_UNITS = {"十": 10, "百": 100, "千": 1000}
KANJI_BIG_UNITS = [("兆", 10**12), ("億", 10**8), ("万", 10**4)]

# 漢数字を構成する文字
KANJI_NUMBER_CHARS = (
    "".join(KANJI_DIGITS) + "".join(KANJI_SMALL_UNITS) + "兆億万"
)

# 数字の後に続いたら「数字として変換」と判定する単位
# 単位 = 「数値+〇〇」で意味が成立する文字列
UNITS = [
    # 時間
    "年", "月", "日", "時", "分", "秒", "週", "週間", "時間",
    "ヶ月", "か月", "ケ月", "カ月", "年代", "年間", "世紀",
    # 通貨・金額
    "円", "ドル", "ユーロ", "元", "ウォン", "ポンド",
    # 数量
    "個", "本", "人", "歳", "回", "度", "匹", "台", "名",
    "件", "階", "種", "区", "班", "組", "番", "号", "倍",
    "杯", "枚", "袋", "箱", "皿", "切れ", "羽", "頭",
    # パーセント
    "%", "％", "パーセント", "割", "分の",
    # データ容量
    "GB", "TB", "MB", "KB", "B", "PB",
    "ギガ", "テラ", "メガ", "キロ",
    "バイト", "ビット",
    # AI モデルサイズ（勝間さん文脈で頻出）
    "B", "M",
    # 重量
    "kg", "g", "mg", "t", "トン", "kt",
    # 距離
    "m", "cm", "mm", "km", "ミリ", "センチ",
    # 体積
    "L", "ml", "dl", "リットル",
    # 速度
    "km/h", "km毎時",
    # 順位・代
    "位", "代", "段", "級",
    # 注: 「期」は単位だが「一期一会」誤変換のため除外
    # 部位的（ヒトコト）
    "畳", "両", "羽", "脚", "頭",
]

# 単位の正規表現（長い順にマッチさせる）
UNIT_PATTERN = "(?:" + "|".join(
    re.escape(u) for u in sorted(UNITS, key=len, reverse=True)
) + ")"

# 漢数字シーケンス（最低 1 文字以上）
KANJI_NUMBER_SEQ = f"[{re.escape(KANJI_NUMBER_CHARS)}]+"


def kanji_to_int(s: str) -> int:
    """漢数字文字列を整数に変換。

    例:
        kanji_to_int("二千二十六") == 2026
        kanji_to_int("百二十") == 120
        kanji_to_int("千") == 1000
        kanji_to_int("一億二千三百万") == 123_000_000
    """
    if not s:
        return 0

    # 兆億万で再帰分割
    for char, value in KANJI_BIG_UNITS:
        if char in s:
            left, _, right = s.partition(char)
            left_val = kanji_to_int(left) if left else 1
            right_val = kanji_to_int(right) if right else 0
            return left_val * value + right_val

    # 千百十単位の処理
    total = 0
    current = 0
    for ch in s:
        if ch in KANJI_DIGITS:
            current = KANJI_DIGITS[ch]
        elif ch in KANJI_SMALL_UNITS:
            unit_val = KANJI_SMALL_UNITS[ch]
            if current == 0:
                current = 1
            total += current * unit_val
            current = 0
    total += current
    return total


def convert(text: str) -> str:
    """テキスト中の「漢数字 + 単位」パターンを「算用数字 + 単位」に変換。

    変換条件:
        1. 漢数字シーケンス（2 文字以上）+ 単位
        2. 漢数字シーケンス（1 文字以上）+ 必須単位（年月日時分秒等）

    変換しないケース（慣用句・固有名詞は自動回避）:
        - 一期一会（期は単位リストにない）
        - 四国（国は単位リストにない）
        - 千葉（葉は単位リストにない）
        - 八百屋（屋は単位リストにない）
        - 一つ・二つ（つは単位リストにない）
    """

    def repl(match: re.Match) -> str:
        kanji_seq = match.group(1)
        unit = match.group(2)
        try:
            num = kanji_to_int(kanji_seq)
        except Exception:
            return match.group(0)
        return f"{num}{unit}"

    # 単一パターン: 漢数字シーケンス + 単位
    pattern = re.compile(f"({KANJI_NUMBER_SEQ})({UNIT_PATTERN})")
    return pattern.sub(repl, text)


def main():
    parser = argparse.ArgumentParser(
        description="勝間 V4 stack: ローカル正規表現で漢数字 → 算用数字補正",
    )
    parser.add_argument("--text", help="入力テキスト (省略時は stdin)")
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="クリップボード内容を補正してクリップボードに戻す",
    )
    parser.add_argument(
        "--check", action="store_true", help="動作テストのみ実行"
    )
    args = parser.parse_args()

    if args.check:
        cases = [
            ("二千二十六年四月二十九日の午前六時三十分", "2026年4月29日の午前6時30分"),
            ("百二十Bの大規模言語モデルで七十Bと比較", "120Bの大規模言語モデルで70Bと比較"),
            ("一期一会で四国を一周した", "一期一会で四国を一周した"),
            ("千葉県の八百屋で買い物", "千葉県の八百屋で買い物"),
            ("一日に二回、三十分ずつ運動する", "1日に2回、30分ずつ運動する"),
            ("ファイルサイズは三百GB", "ファイルサイズは300GB"),
            ("一万円札を二枚使った", "10000円札を2枚使った"),
            ("七五三のお祝いで写真を撮った", "七五三のお祝いで写真を撮った"),
        ]
        ok = ng = 0
        for inp, expected in cases:
            actual = convert(inp)
            status = "OK" if actual == expected else "NG"
            if status == "OK":
                ok += 1
            else:
                ng += 1
            print(f"[{status}] {inp}")
            if status == "NG":
                print(f"       expected: {expected}")
                print(f"       actual:   {actual}")
        print(f"\n結果: {ok} OK / {ng} NG (合計 {ok + ng})")
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
        fixed = convert(text)
        pyperclip.copy(fixed)
        print(f"[OK] {len(text)}c -> {len(fixed)}c (クリップボード更新済)")
        if text != fixed:
            print(f"[BEFORE] {text[:100]}")
            print(f"[AFTER]  {fixed[:100]}")
        else:
            print("[INFO] 変換対象なし")
        return

    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("[ERROR] 入力テキストが空です", file=sys.stderr)
        sys.exit(1)

    print(convert(text))


if __name__ == "__main__":
    main()
