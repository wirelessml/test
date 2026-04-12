#!/bin/bash
# しぶ声ミキサー: キューの音声をFIFOパイプに流す
PIPE="/tmp/shibu-audio"
QUEUE="/tmp/shibu-voice-queue"
FFMPEG="$HOME/local/bin/ffmpeg"

mkdir -p "$QUEUE"
rm -f "$PIPE"
mkfifo "$PIPE"

echo "[mixer] 起動: pipe=$PIPE queue=$QUEUE"

while true; do
    # キューにファイルがあれば再生
    file=$(ls -t "$QUEUE"/*.mp3 2>/dev/null | head -1)
    if [ -n "$file" ]; then
        echo "[mixer] 再生: $(basename $file)"
        "$FFMPEG" -i "$file" -f s16le -ar 44100 -ac 1 pipe:1 2>/dev/null > "$PIPE"
        rm -f "$file"
    else
        # 200msの無音を出力（パイプを生かす）
        dd if=/dev/zero bs=17640 count=1 2>/dev/null > "$PIPE"
    fi
done
