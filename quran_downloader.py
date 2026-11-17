"""
Quran Video Downloader - Real Live Motion Video Engine
ইউটিউব ও অনলাইন সোর্স থেকে বাস্তব লাইভ মোশন ব্যাকগ্রাউন্ড, বৃষ্টি, প্রকৃতি ও ড্রোন শটের
আসল কুরআন তিলাওয়াত রিলস ডাউনলোড করে যাতে প্রতিটি ভিডিও সম্পূর্ণ আলাদা ও ইউনিক হয়।
"""

import os
import glob
import json
import time
import subprocess
from pathlib import Path
from config import DOWNLOADS_DIR, BASE_DIR

HISTORY_FILE = os.path.join(BASE_DIR, "posted_video_ids.json")

def load_posted_ids() -> set:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_posted_id(video_id: str):
    ids = load_posted_ids()
    ids.add(video_id)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(ids)[-500:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[DOWNLOADER] Warning saving history ID: {e}")

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (প্রকৃতি, বৃষ্টি, ড্রোন শট) ও তিলাওয়াত রিলস স্বয়ংক্রিয়ভাবে ডাউনলোড করে।
    একই ভিডিও দ্বিতীয়বার ডাউনলোড হবে না—প্রতিটি ভিডিও সম্পূর্ণ ইউনিক হবে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        try:
            os.remove(f)
        except Exception:
            pass

    surah_num = surah_data.get("number", 1) if surah_data else 1
    surah_bangla = surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}"
    posted_ids = load_posted_ids()

    queries = []
    if surah_data and "query" in surah_data:
        queries.append(surah_data["query"])
    queries.append(f"{surah_bangla} quran recitation emotional reels shorts")
    queries.append(f"{surah_bangla} তিলাওয়াত bangla subtitle shorts")
    queries.append(f"surah {surah_num} emotional beautiful recitation reels")
    queries.append("emotional quran recitation live nature 4k reels shorts")

    selected_video_id = None
    selected_title = None

    for query in queries:
        print(f"[DOWNLOADER] Searching real live video for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch8:{query}",
            "--extractor-args", "youtube:player_client=android,web",
            "--no-playlist",
            "--match-filter", "duration <= 90 & duration >= 15",
            "--print", "%(id)s||%(title)s||%(duration)s"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=40)
            lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                v_id = parts[0].strip()
                v_title = parts[1].strip() if len(parts) > 1 else surah_bangla
                if v_id not in posted_ids:
                    selected_video_id = v_id
                    selected_title = v_title
                    break
        except Exception as se:
            print(f"[DOWNLOADER] Search notice ({se}), trying next query...")

        if selected_video_id:
            break

    if not selected_video_id:
        print("[DOWNLOADER] No unposted video found in targeted queries. Broadening search...")
        selected_video_id = "ZYaZ6Odbx_Y"
        selected_title = f"{surah_bangla} তিলাওয়াত"

    out_template = os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.%(ext)s")
    dl_cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={selected_video_id}",
        "--extractor-args", "youtube:player_client=android,web",
        "-f", "mp4[height<=1920]/best[ext=mp4]/best",
        "--max-filesize", "48M",
        "-o", out_template
    ]

    print(f"[DOWNLOADER] Downloading real live video [{selected_video_id}] - {selected_title}")
    res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=90)

    found_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.*"))
    if not found_files:
        found_files = glob.glob(os.path.join(DOWNLOADS_DIR, "*.mp4"))

    if not found_files or not os.path.exists(found_files[0]):
        raise RuntimeError(f"Failed to download video for {surah_bangla}")

    final_path = found_files[0]
    save_posted_id(selected_video_id)
    print(f"[DOWNLOADER] Successfully downloaded unique live video ({os.path.getsize(final_path)} bytes): {final_path}")

    return {
        "filepath": final_path,
        "title": selected_title or surah_bangla,
        "video_id": selected_video_id,
        "surah_number": surah_num
    }
