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
    
    # Filter duration based on type
    if is_reel:
        duration_filter = "--match-filter duration < 120"
        query = f"ytsearch5:{search_query} #shorts"
    else:
        duration_filter = "--match-filter duration > 180 & duration < 2400"
        query = f"ytsearch5:{search_query}"

    cmd = [
        "yt-dlp",
        "--extractor-args", "youtube:player_client=android,ios",
        "--no-playlist",
        "--max-downloads", "1",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", out_template,
        "--print-json"
    ]
    
    # Add duration filters if specified
    if is_reel:
        cmd.extend(["--match-filter", "duration < 120"])
    else:
        cmd.extend(["--match-filter", "duration > 180 & duration < 2400"])
        
    cmd.append(query)

    print(f"[DOWNLOADER] Searching: {query} (Reel: {is_reel})")
    
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    
    # Check downloaded file in DOWNLOADS_DIR
    files = [os.path.join(DOWNLOADS_DIR, f) for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".mp4")]
    if not files:
        # Fallback without strict duration filter
        print("[DOWNLOADER] Initial filter returned no match, trying fallback query...")
        fallback_query = f"ytsearch3:{search_query}"
        fallback_cmd = [
            "yt-dlp",
            "--extractor-args", "youtube:player_client=android,ios",
            "--no-playlist",
            "--max-downloads", "1",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
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
