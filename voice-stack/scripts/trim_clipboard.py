"""
trim_clipboard.py - 勝間和代式 Python クリップボード自動トリム

原典: 勝間和代 X 投稿 2026-04-15 00:16 (ID 2044072421356113944)
> WhisperモデルでSuperwhisperの方を使うと、自動ペーストの時に一番頭に
> 毎回半角スペースが入って鬱陶しかったので、これがどんなにプロンプトを
> 工夫しても取り除けなかったので、とりあえず出力結果をクリップボードに
> 残して、そのまま自動でペーストする機能を止めて、Pythonで半角スペース
> を除いてからペーストするように順番を変えました。

使い方:
1. SuperWhisper の自動ペースト設定を OFF にする
2. このスクリプトを起動 (python trim_clipboard.py)
3. SuperWhisper でディクテーション → クリップボードに結果が入る
4. このスクリプトが検知 → 半角スペース除去 → 自動ペースト

Ctrl+C で停止
"""

import time
import sys
import pyperclip

try:
    import keyboard
except ImportError:
    print("[ERROR] keyboard モジュールが必要: pip install keyboard")
    sys.exit(1)

POLL_INTERVAL = 0.1  # 秒
last_clipboard = ""


def trim_text(text: str) -> str:
    """先頭・末尾の空白を除去 + 連続空白を 1 つに圧縮"""
    if not text:
        return text
    # 先頭の半角・全角スペース・タブ・改行をすべて除去
    text = text.lstrip(" 　\t\r\n")
    # 末尾の改行を除去（句読点後の改行は残す判断もあるが、勝間方式はトリム）
    text = text.rstrip(" 　\t\r\n")
    return text


def main():
    global last_clipboard
    print("[trim_clipboard] 起動。クリップボードを監視中…")
    print("[trim_clipboard] Ctrl+C で停止")
    last_clipboard = pyperclip.paste()

    while True:
        try:
            current = pyperclip.paste()
            if current and current != last_clipboard:
                trimmed = trim_text(current)
                if trimmed != current:
                    pyperclip.copy(trimmed)
                    print(f"[trim] {len(current)}c -> {len(trimmed)}c: {trimmed[:50]}...")
                    # 自動ペースト (Ctrl+V)
                    time.sleep(0.05)
                    keyboard.send("ctrl+v")
                    last_clipboard = trimmed
                else:
                    last_clipboard = current
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n[trim_clipboard] 停止")
            break
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            time.sleep(1)


if __name__ == "__main__":
    main()
