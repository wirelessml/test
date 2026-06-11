#!/usr/bin/env python3
"""しぶさんのYouTube動画の字幕を一括取得するスクリプト"""

import os
import time
import json
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "transcripts")
INDEX_PATH = os.path.join(OUTPUT_DIR, "index.json")
CHANNEL_URL = "https://www.youtube.com/@minimalist_sibu"


def fetch_videos(limit=200):
    """チャンネルの動画一覧を取得"""
    videos = list(scrapetube.get_channel(channel_url=CHANNEL_URL, limit=limit))
    result = []
    for v in videos:
        vid = v["videoId"]
        title = v.get("title", {}).get("runs", [{}])[0].get("text", "N/A")
        length = v.get("lengthText", {}).get("simpleText", "?")
        result.append({"id": vid, "title": title, "length": length})
    return result


def fetch_transcript(video_id):
    """字幕を取得"""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=["ja"])
    lines = []
    for s in transcript.snippets:
        m = int(s.start // 60)
        sec = int(s.start % 60)
        lines.append(f"[{m:02d}:{sec:02d}] {s.text}")
    return "\n".join(lines)


def save_transcript(video_id, title, length, text):
    """Markdownファイルとして保存"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"yt-{video_id}.md")
    with open(path, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"- URL: https://youtu.be/{video_id}\n")
        f.write(f"- 長さ: {length}\n")
        f.write(f"- チャンネル: ミニマリストしぶ\n\n")
        f.write("## トランスクリプト\n\n")
        f.write("```\n")
        f.write(text)
        f.write("\n```\n")
    return path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 既存のindexを読み込み
    index = {}
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH) as f:
            index = json.load(f)

    # 動画一覧取得
    print("Fetching video list...")
    videos = fetch_videos(200)
    print(f"Found {len(videos)} videos")

    success = 0
    skipped = 0
    failed = 0
    errors = []

    for i, v in enumerate(videos):
        vid = v["id"]
        title = v["title"]

        # 既に取得済みならスキップ
        if vid in index and index[vid].get("status") == "ok":
            skipped += 1
            continue

        print(f"[{i+1}/{len(videos)}] {title[:50]}... ", end="", flush=True)

        try:
            text = fetch_transcript(vid)
            line_count = len(text.split("\n"))
            save_transcript(vid, title, v["length"], text)

            index[vid] = {
                "title": title,
                "length": v["length"],
                "lines": line_count,
                "status": "ok",
            }
            success += 1
            print(f"OK ({line_count} lines)")

        except (NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript) as e:
            index[vid] = {
                "title": title,
                "length": v["length"],
                "status": "no_transcript",
                "error": str(type(e).__name__),
            }
            failed += 1
            errors.append(f"{title}: {type(e).__name__}")
            print(f"SKIP ({type(e).__name__})")

        except Exception as e:
            index[vid] = {
                "title": title,
                "length": v["length"],
                "status": "error",
                "error": str(e)[:100],
            }
            failed += 1
            errors.append(f"{title}: {e}")
            print(f"ERROR ({e})")

        # レート制限対策（IpBlockedを避けるため長めに待機）
        time.sleep(5)

        # indexを定期的に保存
        if (i + 1) % 5 == 0:
            with open(INDEX_PATH, "w") as f:
                json.dump(index, f, ensure_ascii=False, indent=2)

    # 最終index保存
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\n=== DONE ===")
    print(f"Success: {success}")
    print(f"Skipped (already done): {skipped}")
    print(f"Failed/No transcript: {failed}")
    print(f"Total in index: {len(index)}")

    if errors:
        print(f"\nErrors:")
        for e in errors[:10]:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
