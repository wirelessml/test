#!/bin/bash
# 面談 文字起こし v2（whisper.cpp / large-v3-turbo、ローカル・無料）
#
# 使い方: このファイルをダブルクリックするだけ。最新の録音を自動で選んで処理します。
#
# 優先順位:
#   1) ~/面談録画/ の「面談-*-自分.wav / -相手.wav」ペア（v3 別トラック録画）
#      → それぞれ文字起こし ＋ 【自分】【相手】ラベル付きの会話テキストを自動生成
#   2) ~/面談録音/ の最新 wav/m4a（旧・音声のみ録音）
#   3) ~/面談録画/ の最新 mp4（ミックス音声）
#
# 出力: 素材と同じフォルダに .txt / .srt（ペアの場合はさらに -会話.txt）
#
# ※ v2 変更点: 繰り返し幻覚対策の -mc 0 を常時適用（6/11 GVC面談の教訓）

set -u
MODEL="$HOME/whisper-models/ggml-large-v3-turbo.bin"
[ -f "$MODEL" ] || MODEL="$HOME/whisper-models/ggml-medium.bin"
WCLI="/opt/homebrew/bin/whisper-cli"
FFMPEG="$HOME/local/bin/ffmpeg"

transcribe() {  # $1=音声ファイル $2=出力ベース名(拡張子なし)
  local TMP="/tmp/whisper_in_$$_$RANDOM.wav"
  "$FFMPEG" -y -hide_banner -loglevel error -i "$1" -vn -ar 16000 -ac 1 "$TMP" || return 1
  "$WCLI" -m "$MODEL" -f "$TMP" -l ja -mc 0 -otxt -osrt -of "$2" >/dev/null 2>&1
  rm -f "$TMP"
}

MIC="$(ls -t "$HOME/面談録画/"*-自分.wav 2>/dev/null | head -1)"

if [ -n "${MIC:-}" ] && [ -f "$MIC" ]; then
  BASE="${MIC%-自分.wav}"
  REM="$BASE-相手.wav"
  echo "=================================================="
  echo "  別トラック文字起こし: $(basename "$BASE")"
  echo "  （自分→相手の順に処理。30分録音で計10分ほど）"
  echo "=================================================="
  echo "[1/3] 自分の声 …"
  transcribe "$MIC" "$BASE-自分"
  echo "[2/3] 相手の声 …"
  transcribe "$REM" "$BASE-相手"
  echo "[3/3] 会話テキストに合成 …"
  /usr/bin/python3 - "$BASE-自分.srt" "$BASE-相手.srt" "$BASE-会話.txt" << 'PYEOF'
import sys, re

def parse_srt(path, label):
    try:
        raw = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return []
    items = []
    for block in re.split(r'\n\s*\n', raw.strip()):
        lines = block.strip().split('\n')
        if len(lines) >= 3 and '-->' in lines[1]:
            m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+)', lines[1])
            if not m:
                continue
            sec = int(m[1])*3600 + int(m[2])*60 + int(m[3]) + int(m[4])/1000
            text = ' '.join(lines[2:]).strip()
            if text:
                items.append((sec, label, text))
    return items

a = parse_srt(sys.argv[1], '自分')
b = parse_srt(sys.argv[2], '相手')
merged = sorted(a + b, key=lambda x: x[0])
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    prev = None
    for sec, label, text in merged:
        t = f'{int(sec//60):02d}:{int(sec%60):02d}'
        if label != prev:
            f.write(f'\n【{label}】\n')
            prev = label
        f.write(f'{t} {text}\n')
print(f'  会話テキスト: {len(merged)}発言')
PYEOF
  echo ""
  echo "■ 完了:"
  echo "   会話（ラベル付き）→ $BASE-会話.txt"
  echo "   自分のみ → $BASE-自分.txt / 相手のみ → $BASE-相手.txt"
  open "$BASE-会話.txt" 2>/dev/null
  exit 0
fi

# フォールバック: 旧録音 or ミックスmp4
SRC="$(ls -t "$HOME/面談録音/"*.wav "$HOME/面談録音/"*.m4a "$HOME/面談録画/"*.mp4 2>/dev/null | head -1)"
if [ -z "${SRC:-}" ] || [ ! -f "$SRC" ]; then
  echo "❌ 文字起こしする録音が見つかりません。"
  echo "   先に「面談-録画.command」で録画してください。"
  read -n1 -r -p "Enterで閉じる…" _; exit 1
fi
BASE="${SRC%.*}"
echo "=================================================="
echo "  文字起こし中: $(basename "$SRC")"
echo "=================================================="
transcribe "$SRC" "$BASE"
echo ""
echo "■ 完了: ${BASE}.txt / ${BASE}.srt"
open "${BASE}.txt" 2>/dev/null
