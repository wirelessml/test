#!/usr/bin/env python3
"""YouTube動画の字幕を取得してMarkdownで保存するスクリプト"""

import sys
import os
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url_or_id: str) -> str:
    """URLまたはIDからvideo IDを抽出"""
    if "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]
    return url_or_id


def fetch_transcript(video_id: str) -> str:
    """字幕を取得して連結テキストで返す"""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=["ja"])
    lines = []
    for s in transcript.snippets:
        minutes = int(s.start // 60)
        seconds = int(s.start % 60)
        lines.append(f"[{minutes:02d}:{seconds:02d}] {s.text}")
    return "\n".join(lines)


def save_as_markdown(video_id: str, transcript_text: str, output_dir: str):
    """Markdownファイルとして保存"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"yt-{video_id}.md")
    with open(path, "w") as f:
        f.write(f"# YouTube字幕: {video_id}\n\n")
        f.write(f"https://youtu.be/{video_id}\n\n")
        f.write("## トランスクリプト\n\n")
        f.write("```\n")
        f.write(transcript_text)
        f.write("\n```\n")
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 youtube-transcript.py <VIDEO_URL_OR_ID> [OUTPUT_DIR]")
        sys.exit(1)

    video_id = extract_video_id(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "../knowledge/transcripts"

    print(f"Fetching transcript for: {video_id}")
    text = fetch_transcript(video_id)
    line_count = len(text.split("\n"))
    print(f"Got {line_count} lines")

    save_as_markdown(video_id, text, output_dir)
