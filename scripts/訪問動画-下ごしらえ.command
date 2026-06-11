#!/bin/bash
# 訪問動画 下ごしらえ — iPhone動画 ＋（あれば）Mac別録り音声 を合成し、字幕SRT＋全文テキストまで自動生成
#
# 【使い方】
#   1) iPhone で撮った動画を AirDrop で Mac に送り、~/Desktop/訪問動画素材/ に入れる
#      （Mac で別録りした音声 wav があれば同じフォルダへ。無くてもOK）
#   2) このファイルをダブルクリック
#   3) 音ズレ補正を聞かれたら秒数を入力（不要なら Enter）
#
# 【出力（同じフォルダ）】
#   <動画名>-下ごしらえ.mp4 … 映像無劣化＋音声ミックス（iMovie に持ち込む本番素材）
#   <動画名>-下ごしらえ.srt … タイムスタンプ付き字幕（カット点探し・テロップ起こし用）
#   <動画名>-下ごしらえ.txt … 全文テキスト
#
# ※ 映像は再エンコードしない（無劣化コピー、6/10 imovie-min-test で実証した方式）
# ※ 文字起こしは whisper.cpp large-v3-turbo / -mc 0（繰り返し幻覚対策）

set -u
FFMPEG="$HOME/local/bin/ffmpeg"
WCLI="/opt/homebrew/bin/whisper-cli"
MODEL="$HOME/whisper-models/ggml-large-v3-turbo.bin"
[ -f "$MODEL" ] || MODEL="$HOME/whisper-models/ggml-medium.bin"
DIR="$HOME/Desktop/訪問動画素材"
mkdir -p "$DIR"

# 最新の動画（下ごしらえ済みは除外）
VID="$(ls -t "$DIR"/*.mp4 "$DIR"/*.mov "$DIR"/*.MOV "$DIR"/*.MP4 2>/dev/null | grep -v '下ごしらえ' | head -1)"
if [ -z "${VID:-}" ] || [ ! -f "$VID" ]; then
  echo "❌ 動画が見つかりません。iPhone の動画を AirDrop して"
  echo "   $DIR に入れてから、もう一度ダブルクリックしてください。"
  read -n1 -r -p "Enterで閉じる…" _; exit 1
fi
WAV="$(ls -t "$DIR"/*.wav 2>/dev/null | head -1)"

NAME="$(basename "${VID%.*}")"
OUT="$DIR/$NAME-下ごしらえ.mp4"

echo "=================================================="
echo "  訪問動画 下ごしらえ"
echo "  動画: $(basename "$VID")"
if [ -n "${WAV:-}" ]; then echo "  Mac音声: $(basename "$WAV")"; else echo "  Mac音声: なし（動画の音声をそのまま使用）"; fi
echo "=================================================="

if [ -n "${WAV:-}" ] && [ -f "$WAV" ]; then
  echo ""
  echo "音ズレ補正: Mac音声を何秒「遅らせ」ますか？"
  echo "（動画よりMac録音を後に開始した場合はマイナス値。例: 1.5 / -2 / そのままEnter=0）"
  read -r -p "> " OFFSET
  OFFSET="${OFFSET:-0}"

  # 動画側に音声トラックがあるか
  if "$FFMPEG" -hide_banner -i "$VID" 2>&1 | grep -q 'Audio:'; then HASAUDIO=1; else HASAUDIO=0; fi

  echo "[1/2] 合成中…（映像は無劣化コピー）"
  if [ "$HASAUDIO" = "1" ]; then
    if [ "$(echo "$OFFSET >= 0" | bc -l)" = "1" ]; then
      MS=$(echo "$OFFSET * 1000 / 1" | bc)
      "$FFMPEG" -y -hide_banner -loglevel error -i "$VID" -i "$WAV" \
        -filter_complex "[1:a]adelay=${MS}:all=1[d];[0:a][d]amix=inputs=2:duration=first:normalize=0[a]" \
        -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "$OUT"
    else
      SS=$(echo "-1 * $OFFSET" | bc -l)
      "$FFMPEG" -y -hide_banner -loglevel error -i "$VID" -ss "$SS" -i "$WAV" \
        -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[a]" \
        -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "$OUT"
    fi
  else
    # 動画に音が無い場合は Mac音声をそのまま載せる
    "$FFMPEG" -y -hide_banner -loglevel error -i "$VID" -i "$WAV" \
      -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
  fi
else
  echo "[1/2] Mac音声なし → 動画をそのままコピー"
  cp "$VID" "$OUT"
fi

[ -s "$OUT" ] || { echo "❌ 合成に失敗しました"; read -n1 -r -p "Enterで閉じる…" _; exit 1; }

echo "[2/2] 文字起こし中…（whisper、動画の長さの約1/5の時間）"
TMP="/tmp/whisper_visit_$$.wav"
"$FFMPEG" -y -hide_banner -loglevel error -i "$OUT" -vn -ar 16000 -ac 1 "$TMP"
"$WCLI" -m "$MODEL" -f "$TMP" -l ja -mc 0 -otxt -osrt -of "${OUT%.mp4}" >/dev/null 2>&1
rm -f "$TMP"

echo ""
echo "■ 完了:"
echo "   本番素材 → $OUT"
echo "   字幕     → ${OUT%.mp4}.srt"
echo "   全文     → ${OUT%.mp4}.txt"
echo ""
echo "次: $OUT を iMovie に読み込んでカット・テロップ（SRTを横に開いて使う）"
open -R "$OUT" 2>/dev/null
