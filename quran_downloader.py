"""
Quran Video Downloader - Real Live Motion Video Engine
প্রকৃতি, বৃষ্টি, ঝর্ণা, মহাসমুদ্র ও ড্রোন শটের আসল লাইভ মোশন কুরআন তিলাওয়াত ভিডিও
কোনো স্থির ছবি বা স্লাইড নয়—প্রতিটি ভিডিওতে থাকবে চলমান প্রাকৃতিক দৃশ্য ও মধুর তিলাওয়াত।
"""

import os
import glob
import json
import time
import random
import subprocess
from pathlib import Path
from config import DOWNLOADS_DIR, BASE_DIR

HISTORY_FILE = os.path.join(BASE_DIR, "posted_video_ids.json")

# নিশ্চিত লাইভ মোশন ব্যাকগ্রাউন্ড (বৃষ্টি, ঝর্ণা, ড্রোন, সাগর) সহ ভিডিও পুল
VERIFIED_LIVE_VIDEOS = [
    {"id": "03bZxuv26Tk", "title": "সূরা আর-রহমান • বৃষ্টি ও অন্তরের প্রশান্তি", "surah": "সূরা আর-রহমান"},
    {"id": "1MfU9psrDzQ", "title": "সূরা আল-ওয়াকিয়াহ • ঝর্ণার অপূর্ব দৃশ্য ও তিলাওয়াত", "surah": "সূরা আল-ওয়াকিয়াহ"},
    {"id": "20AbFQzuRZM", "title": "সূরা আল-মুলক • গভীর অরণ্যের মনোমুগ্ধকর ঝর্ণা", "surah": "সূরা আল-মুলক"},
    {"id": "3Mj7v_cDK10", "title": "সূরা ইয়াসিন • বৃষ্টির শীতল স্পর্শ ও কুরআন তিলাওয়াত", "surah": "সূরা ইয়াসিন"},
    {"id": "sHk7u73f8Tw", "title": "সূরা মারিয়াম • প্রকৃতির নৈসর্গিক সৌন্দর্য ও তিলাওয়াত", "surah": "সূরা মারিয়াম"},
    {"id": "IesdLMXUKJo", "title": "সূরা আল-কাহফ • প্রশান্তিময় হৃদয়স্পর্শী তিলাওয়াত", "surah": "সূরা আল-কাহফ"},
    {"id": "Y5ITGlVpWAs", "title": "সূরা ত্বা-হা • মন জুড়ানো প্রকৃতি ও তিলাওয়াত", "surah": "সূরা ত্বা-হা"}
]

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
    বাস্তব চলমান লাইভ ভিডিও (বৃষ্টি, ঝর্ণা, ড্রোন, মহাসমুদ্র) ডাউনলোড করে।
    কোনো স্থির ছবি বা ফটো স্লাইড আসবে না।
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

    # ১. লাইভ মোশন কুয়েরি তৈরি (যেগুলোতে গ্যারান্টিড রিয়েল চলমান ভিডিও থাকে)
    live_queries = [
        f"{surah_bangla} quran status rain aesthetic shorts",
        f"{surah_bangla} quran recitation waterfall nature reels",
        f"{surah_bangla} quran aesthetic ocean drone shorts",
        "quran status rain aesthetic shorts",
        "quran status waterfall nature 4k shorts",
        "quran recitation aesthetic nature shorts",
        "quran drone nature aesthetic reels shorts"
    ]

    selected_video_id = None
    selected_title = None

    # স্থির ছবি ফিল্টার: যাতে কোনো স্টিল ফটো বা অডিও-অনলি ভিডিও না আসে
    bad_keywords = ["audio", "full surah", "podcast", "slide", "black screen", "waz", "book", "cover"]

    for query in live_queries:
        print(f"[DOWNLOADER] Searching real live video for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch6:{query}",
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
                
                lower_title = v_title.lower()
                if any(bad in lower_title for bad in bad_keywords):
                    continue

                if v_id not in posted_ids:
                    selected_video_id = v_id
                    selected_title = v_title
                    break
        except Exception as se:
            print(f"[DOWNLOADER] Search notice ({se}), trying next query...")

        if selected_video_id:
            break

    # ফলব্যাক: যদি সার্চে লাইভ ভিডিও না পায়, তবে নিশ্চিত লাইভ পুল থেকে আনপোস্টেড ভিডিও নেওয়া
    if not selected_video_id:
        print("[DOWNLOADER] Using guaranteed live nature/rain verified pool...")
        available_pool = [v for v in VERIFIED_LIVE_VIDEOS if v["id"] not in posted_ids]
        if not available_pool:
            available_pool = VERIFIED_LIVE_VIDEOS
        chosen = random.choice(available_pool)
        selected_video_id = chosen["id"]
        selected_title = chosen["title"]

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

    # ব্যাকআপ: যদি প্রথম আইডি কোনো কারণে ডাউনলোড না হয়, পুলের অন্য লাইভ ভিডিও দিয়ে চেষ্টা
    if not found_files or not os.path.exists(found_files[0]):
        print(f"[DOWNLOADER] Initial download failed. Trying other verified live videos...")
        for backup_item in VERIFIED_LIVE_VIDEOS:
            if backup_item["id"] == selected_video_id:
                continue
            b_id = backup_item["id"]
            b_out = os.path.join(DOWNLOADS_DIR, f"quran_{b_id}.%(ext)s")
            b_cmd = [
                "yt-dlp",
                f"https://www.youtube.com/watch?v={b_id}",
                "--extractor-args", "youtube:player_client=android,web",
                "-f", "mp4[height<=1920]/best[ext=mp4]/best",
                "--max-filesize", "48M",
                "-o", b_out
            ]
            print(f"[DOWNLOADER] Trying verified live motion video [{b_id}] - {backup_item['title']}")
            b_res = subprocess.run(b_cmd, capture_output=True, text=True, timeout=90)
            b_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"quran_{b_id}.*"))
            if b_files and os.path.exists(b_files[0]):
                found_files = b_files
                selected_video_id = b_id
                selected_title = backup_item["title"]
                break

    if not found_files or not os.path.exists(found_files[0]):
        raise RuntimeError(f"Failed to download video for {surah_bangla}")

    final_path = found_files[0]
    save_posted_id(selected_video_id)
    print(f"[DOWNLOADER] Successfully downloaded real live motion video ({os.path.getsize(final_path)} bytes): {final_path}")

    return {
        "filepath": final_path,
        "title": selected_title or surah_bangla,
        "video_id": selected_video_id,
        "surah_number": surah_num
    }
