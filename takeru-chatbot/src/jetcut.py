#!/usr/bin/env python3
"""
しぶチャンネル式 自動ジェットカットスクリプト
- 音声波形を解析して無音部分を自動カット
- BGM・効果音なし（ミニマリズム編集哲学）
- ffmpegベースで高速処理

Usage:
    python3 jetcut.py input.mp4 [--output output.mp4] [--silence-thresh -35] [--min-silence 0.4] [--padding 0.1]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FFMPEG = os.path.expanduser("~/local/bin/ffmpeg")


def detect_silence(input_path, silence_thresh=-35, min_silence_len=0.4):
    """ffmpegのsilencedetectフィルタで無音区間を検出"""
    cmd = [
        FFMPEG, "-i", input_path,
        "-af", f"silencedetect=noise={silence_thresh}dB:d={min_silence_len}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    silences = []
    start = None
    for line in stderr.split("\n"):
        if "silence_start:" in line:
            start = float(line.split("silence_start:")[1].strip().split()[0])
        elif "silence_end:" in line and start is not None:
            end = float(line.split("silence_end:")[1].strip().split()[0])
            silences.append((start, end))
            start = None

    return silences


def get_duration(input_path):
    """動画の総時間を取得"""
    cmd = [
        FFMPEG, "-i", input_path,
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.split("\n"):
        if "Duration:" in line:
            time_str = line.split("Duration:")[1].strip().split(",")[0]
            parts = time_str.split(":")
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return 0


def silences_to_segments(silences, duration, padding=0.1):
    """無音区間から発話区間（残す部分）を算出"""
    segments = []
    prev_end = 0.0

    for silence_start, silence_end in silences:
        seg_start = prev_end
        seg_end = silence_start + padding  # 無音の直前まで + パディング

        if seg_end > seg_start + 0.05:  # 極端に短いセグメントは除外
            segments.append((max(0, seg_start), min(seg_end, duration)))

        prev_end = silence_end - padding  # 無音の直後から - パディング

    # 最後のセグメント
    if prev_end < duration - 0.05:
        segments.append((max(0, prev_end), duration))

    return segments


def merge_short_gaps(segments, min_gap=0.15):
    """近すぎるセグメントを結合"""
    if not segments:
        return segments

    merged = [segments[0]]
    for start, end in segments[1:]:
        prev_start, prev_end = merged[-1]
        if start - prev_end < min_gap:
            merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))
    return merged


def export_with_concat(input_path, segments, output_path):
    """ffmpegのconcatフィルタで発話部分を連結して書き出し"""
    if not segments:
        print("ERROR: No segments to export")
        return False

    # セグメントごとにtrim+atrateフィルタを構築
    filter_parts = []
    concat_inputs = []

    for i, (start, end) in enumerate(segments):
        filter_parts.append(
            f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={start:.3f}:end={end:.3f},asetpts=PTS-STARTPTS[a{i}];"
        )
        concat_inputs.append(f"[v{i}][a{i}]")

    n = len(segments)
    filter_complex = "".join(filter_parts)
    filter_complex += "".join(concat_inputs) + f"concat=n={n}:v=1:a=1[outv][outa]"

    cmd = [
        FFMPEG, "-y", "-i", input_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        output_path
    ]

    print(f"\nExporting {len(segments)} segments...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        # セグメント数が多い場合はファイル分割方式にフォールバック
        print("concat filter too complex, falling back to file-based concat...")
        return export_with_file_concat(input_path, segments, output_path)

    return True


def export_with_file_concat(input_path, segments, output_path):
    """セグメントが多い場合: 個別ファイルに書き出してからconcat"""
    tmpdir = tempfile.mkdtemp(prefix="jetcut_")
    file_list = os.path.join(tmpdir, "files.txt")
    segment_files = []

    print(f"Exporting {len(segments)} segments individually...")

    for i, (start, end) in enumerate(segments):
        seg_file = os.path.join(tmpdir, f"seg_{i:04d}.ts")
        cmd = [
            FFMPEG, "-y", "-i", input_path,
            "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "mpegts", seg_file
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        segment_files.append(seg_file)

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(segments)} segments done...")

    # concat
    with open(file_list, "w") as f:
        for sf in segment_files:
            f.write(f"file '{sf}'\n")

    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", file_list,
        "-c", "copy", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # cleanup
    for sf in segment_files:
        os.remove(sf)
    os.remove(file_list)
    os.rmdir(tmpdir)

    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="しぶチャンネル式 自動ジェットカット")
    parser.add_argument("input", help="入力動画ファイル")
    parser.add_argument("--output", "-o", help="出力ファイル（デフォルト: input_jetcut.mp4）")
    parser.add_argument("--silence-thresh", "-t", type=float, default=-35,
                        help="無音判定の閾値 (dB, デフォルト: -35)")
    parser.add_argument("--min-silence", "-s", type=float, default=0.4,
                        help="無音と判定する最小の長さ (秒, デフォルト: 0.4)")
    parser.add_argument("--padding", "-p", type=float, default=0.1,
                        help="カット前後のパディング (秒, デフォルト: 0.1)")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="分析のみ、書き出しなし")
    parser.add_argument("--stats", action="store_true",
                        help="詳細な統計を表示")
    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found")
        sys.exit(1)

    if not args.output:
        stem = Path(input_path).stem
        args.output = str(Path(input_path).parent / f"{stem}_jetcut.mp4")

    # Step 1: 動画情報取得
    duration = get_duration(input_path)
    print(f"Input: {input_path}")
    print(f"Duration: {duration:.1f}s ({duration/60:.1f}min)")

    # Step 2: 無音検出
    print(f"\nDetecting silence (thresh={args.silence_thresh}dB, min={args.min_silence}s)...")
    silences = detect_silence(input_path, args.silence_thresh, args.min_silence)
    print(f"Found {len(silences)} silent sections")

    # Step 3: 発話セグメント算出
    segments = silences_to_segments(silences, duration, args.padding)
    segments = merge_short_gaps(segments)

    # 統計
    total_speech = sum(end - start for start, end in segments)
    total_silence = duration - total_speech
    cut_ratio = (1 - total_speech / duration) * 100 if duration > 0 else 0

    print(f"\n{'='*50}")
    print(f"  Segments (speech): {len(segments)}")
    print(f"  Speech time:       {total_speech:.1f}s ({total_speech/60:.1f}min)")
    print(f"  Silence removed:   {total_silence:.1f}s ({total_silence/60:.1f}min)")
    print(f"  Cut ratio:         {cut_ratio:.1f}%")
    print(f"  Output duration:   {total_speech:.1f}s ({total_speech/60:.1f}min)")
    print(f"{'='*50}")

    if args.stats:
        print("\nSegments detail:")
        for i, (s, e) in enumerate(segments):
            print(f"  [{i+1:4d}] {s:8.2f}s - {e:8.2f}s ({e-s:.2f}s)")

    if args.dry_run:
        print("\n(dry-run mode, skipping export)")
        return

    # Step 4: 書き出し
    success = export_with_concat(input_path, segments, args.output)

    if success and os.path.exists(args.output):
        out_size = os.path.getsize(args.output) / 1024 / 1024
        print(f"\nOutput: {args.output} ({out_size:.1f}MB)")
        print("Done!")
    else:
        print("\nERROR: Export failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
