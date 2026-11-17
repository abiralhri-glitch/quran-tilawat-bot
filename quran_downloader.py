"""
Quran Video Downloader using yt-dlp
ইউটিউব ও অন্যান্য ইসলামিক আর্কাইভ থেকে সর্বোচ্চ কোয়ালিটির তিলাওয়াত ভিডিও ও রিলস ডাউনলোড
"""

import os
import subprocess
import json
import glob
from config import DOWNLOADS_DIR

def download_quran_video(search_query: str, is_reel: bool = True) -> dict:
    """
    Search and download a Quran recitation video.
    If is_reel is True, search for short 9:16 vertical reels (< 90 seconds).
    If is_reel is False, search for full Surah videos (5 - 30 minutes).
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    
    # Clean previous temp downloads
    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        try:
            os.remove(f)
        except Exception:
            pass

    out_template = os.path.join(DOWNLOADS_DIR, "%(id)s.%(ext)s")
    
    if is_reel:
        query = f"ytsearch1:{search_query} shorts"
    else:
        query = f"ytsearch1:{search_query}"

    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--merge-output-format", "mp4",
        "--max-filesize", "150M",
        "-o", out_template,
        query
    ]

    print(f"[DOWNLOADER] Downloading via yt-dlp: '{query}'")
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    
    # Check downloaded file in DOWNLOADS_DIR
    files = [os.path.join(DOWNLOADS_DIR, f) for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".mp4")]
    if not files:
        # Fallback query
        print("[DOWNLOADER] Initial search returned no file, trying fallback...")
        fallback_query = "ytsearch1:quran tilawat bangla subtitle shorts"
        fallback_cmd = [
            "yt-dlp",
            "--no-warnings",
            "--merge-output-format", "mp4",
            "--max-filesize", "150M",
            "-o", out_template,
            fallback_query
        ]
        subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        files = [os.path.join(DOWNLOADS_DIR, f) for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".mp4")]

    if not files:
        raise RuntimeError(f"Failed to download video for query: {search_query}. Error: {process.stderr[:200]}")

    video_path = files[0]
    
    metadata = {
        "filepath": video_path,
        "title": search_query,
        "is_reel": is_reel
    }
    
    # Try parsing stdout json
    for line in process.stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                info = json.loads(line)
                metadata["title"] = info.get("title", search_query)
                metadata["duration"] = info.get("duration", 0)
                metadata["uploader"] = info.get("uploader", "")
                break
            except Exception:
                pass

    print(f"[DOWNLOADER] Successfully downloaded: {video_path} (Title: {metadata['title']})")
    return metadata
