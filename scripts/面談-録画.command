#!/bin/bash
# 面談 録画 v3 — 画面 ＋ 自分の声 ＋ 相手の声 を「別トラック」で記録し、再生用MP4も自動生成
#
# 【事前準備（面談の前に1回だけ）】
#   ・システム設定 > サウンド > 出力 を「複数出力装置」に切替
#     （EarPodsで相手の声を聞きながら、BlackHoleにも同じ音を流す＝相手の声を録音するため）
#   ・Zoom / Google Meet は普通に参加するだけでOK（ブラウザ参加でも可）
#
# 【録画する】
#   1) このファイルをダブルクリック → すぐ録画開始
#   2) 面談する
#   3) 止めるには このターミナル窓で  Control + C  を1回
#      → 自動で仕上げ処理が走ります（数十秒〜数分待つ）
#
# 【出力（~/面談録画/）】
#   面談-<日時>.mp4        … 画面 + ミックス音声（普通に再生する用）
#   面談-<日時>-自分.wav   … マイクの音だけ（文字起こし用）
#   面談-<日時>-相手.wav   … 相手の声だけ（文字起こし用・後から音量調整可能）
#
# 文字起こしは「面談-文字起こし.command」をダブルクリック（自分/相手ラベル付きで出ます）
#
# ※ v2(GVC版)からの変更: 音声を別トラック記録に（相手の声が小さくても後から救える）
# ※ 画面は macOS 標準 screencapture（ffmpegの画面キャプチャはmacOSでハングするため）

FFMPEG="$HOME/local/bin/ffmpeg"
DIR="$HOME/面談録画"
mkdir -p "$DIR"
TS=$(date +%Y%m%d-%H%M%S)
VID="$DIR/.tmp-screen-$TS.mov"
MIC="$DIR/面談-$TS-自分.wav"
REM="$DIR/面談-$TS-相手.wav"
OUT="$DIR/面談-$TS.mp4"

echo "=================================================="
echo "   ● 録画中 …（画面 ＋ 自分の声 ＋ 相手の声 別録り）"
echo "   保存先: $OUT"
echo ""
echo "   ■ 止めるには  Control + C  を1回押す"
echo "     （押した後、仕上げが終わるまで窓を閉じない）"
echo "=================================================="
echo ""

# Ctrl+C で screencapture / ffmpeg は止まるが、このスクリプト自身は生き残って仕上げへ進む
trap 'true' INT

# 音声: マイクと BlackHole(相手の声) を1プロセスで別ファイルに同時記録（WAV=壊れにくい）
"$FFMPEG" -hide_banner -loglevel error \
  -f avfoundation -i ":MacBook Airのマイク" \
  -f avfoundation -i ":BlackHole 2ch" \
  -map 0:a -ac 1 "$MIC" \
  -map 1:a -ac 1 "$REM" &
AUDIO_PID=$!

# 画面: macOS 標準の収録（Ctrl+C で確定保存される）
screencapture -x -v "$VID"

# Ctrl+C 後: 音声側の終了を待つ
wait $AUDIO_PID 2>/dev/null

echo ""
echo "■ 録画停止。再生用MP4を作成中…"

# 仕上げ: 映像は無劣化コピー、音声は2トラックをミックスしてAAC化
"$FFMPEG" -hide_banner -loglevel error -y \
  -i "$VID" -i "$MIC" -i "$REM" \
  -filter_complex "[1:a][2:a]amix=inputs=2:duration=longest:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k \
  -shortest "$OUT"

if [ -s "$OUT" ]; then
  rm -f "$VID"
  echo ""
  echo "■ 保存しました:"
  echo "   再生用 → $OUT"
  echo "   自分の声 → $MIC"
  echo "   相手の声 → $REM"
else
  echo ""
  echo "⚠️ MP4作成に失敗。素材は残してあります:"
  echo "   画面: $VID / 自分: $MIC / 相手: $REM"
fi
echo "（このウィンドウは閉じてOK。文字起こしは 面談-文字起こし.command で）"
