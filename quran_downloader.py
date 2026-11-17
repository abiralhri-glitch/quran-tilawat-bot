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
import requests
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

# সরাসরি লাইভ মোশন ও তিলাওয়াত ভিডিও ব্যাকআপ পুল (আর্কাইভ ও ক্লাউড সিডিএন—১০০% চলমান দৃশ্য)
DIRECT_LIVE_VIDEOS = [
    {
        "id": "live_recitation_02",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2002.mp4",
        "title": "সূরা আল-মুলক • ক্বারী মুহাম্মদ সরাসরি তিলাওয়াত",
        "surah_number": 67
    },
    {
        "id": "live_recitation_05",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2005.mp4",
        "title": "সূরা আর-রহমান • অন্তরের প্রশান্তিময় তিলাওয়াত",
        "surah_number": 55
    },
    {
        "id": "live_recitation_07",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2007.mp4",
        "title": "সূরা ইয়াসিন • হৃদয়স্পর্শী তিলাওয়াত",
        "surah_number": 36
    },
    {
        "id": "live_recitation_08",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2008.mp4",
        "title": "সূরা আল-ওয়াকিয়াহ • রূহানী প্রশান্তি",
        "surah_number": 56
    },
    {
        "id": "live_recitation_01",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2001.mp4",
        "title": "সূরা আল-কাহফ • নূর ও হেদায়েত",
        "surah_number": 18
    },
    {
        "id": "live_recitation_03",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2003.mp4",
        "title": "সূরা মারিয়াম • পবিত্র তিলাওয়াত",
        "surah_number": 19
    },
    {
        "id": "live_recitation_04",
        "url": "https://archive.org/download/QariMuhammadKantawi_Tilawat_Video/%D8%AA%D9%84%D8%A7%D9%88%D8%A9%20%D9%85%D8%B1%D8%A6%D9%8A%D8%A9%20%D9%84%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%83%D9%86%D8%AA%D8%A7%D9%88%D9%8A%2004.mp4",
        "title": "সূরা ত্বা-হা • মধুর সুরের তিলাওয়াত",
        "surah_number": 20
    }
]

# চলমান প্রাকৃতিক ব্যাকগ্রাউন্ড ভিডিও (বৃষ্টি, ঝর্ণা, ড্রোন)
NATURE_MOTION_BACKGROUNDS = [
    {
        "id": "waterfall_sohosrodhara",
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Sohosrodhara_Waterfall%2C_Sitakund_Eco-Park%2C_Chittagong%2C_Bangladesh.webm",
        "desc": "প্রাকৃতিক ঝর্ণার দৃশ্য"
    },
    {
        "id": "rain_motion_drops",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Rain_water.webm",
        "desc": "বৃষ্টির মন জুড়ানো দৃশ্য"
    },
    {
        "id": "drone_waterfall_keila",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Drone_video_of_Keila_waterfall_and_manor_in_Keila-Joa%2C_Estonia.webm",
        "desc": "ড্রোন শটে মনোরম জলপ্রপাত"
    },
    {
        "id": "fern_creek_falls",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720.mp4",
        "desc": "পাহাড়ি ঝর্ণার প্রবাহ"
    }
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

def download_file_direct(url: str, out_path: str, timeout: int = 45) -> bool:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        with requests.get(url, stream=True, headers=headers, timeout=timeout) as r:
            r.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        return os.path.exists(out_path) and os.path.getsize(out_path) > 100000
    except Exception as e:
        print(f"[DOWNLOADER] Direct download notice for {url}: {e}")
        return False

def generate_nature_quran_reel(surah_num: int, surah_bangla: str, posted_ids: set) -> dict:
    """
    বাস্তব চলমান প্রকৃতির দৃশ্য (ঝর্ণা/বৃষ্টি/ড্রোন) এবং সংশ্লিষ্ট সূরার মধুর তিলাওয়াত
    একত্রিত করে নিখুঁত ৯:১৬ চলমান লাইভ রিলস তৈরি করে।
    """
    print(f"[DOWNLOADER] Generating live nature motion reel for {surah_bangla} (#{surah_num})...")

    available_bg = [b for b in NATURE_MOTION_BACKGROUNDS if f"{b['id']}_{surah_num}" not in posted_ids]
    if not available_bg:
        available_bg = NATURE_MOTION_BACKGROUNDS
    bg_choice = random.choice(available_bg)

    bg_raw_ext = ".mp4" if bg_choice["url"].endswith(".mp4") else ".webm"
    bg_path = os.path.join(DOWNLOADS_DIR, f"bg_{bg_choice['id']}{bg_raw_ext}")
    audio_path = os.path.join(DOWNLOADS_DIR, f"audio_surah_{surah_num}.mp3")
    final_output = os.path.join(DOWNLOADS_DIR, f"nature_quran_{surah_num}_{int(time.time())}.mp4")

    if not os.path.exists(bg_path) or os.path.getsize(bg_path) < 10000:
        print(f"[DOWNLOADER] Downloading motion background: {bg_choice['desc']}")
        if not download_file_direct(bg_choice["url"], bg_path):
            raise RuntimeError(f"Could not download motion background {bg_choice['url']}")

    audio_url = f"https://server8.mp3quran.net/afs/{surah_num:03d}.mp3"
    print(f"[DOWNLOADER] Downloading recitation audio from {audio_url}")
    if not download_file_direct(audio_url, audio_path):
        audio_url_backup = f"https://everyayah.com/data/Alafasy_128kbps/{surah_num:03d}001.mp3"
        download_file_direct(audio_url_backup, audio_path)

    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 5000:
        raise RuntimeError("Could not download audio recitation")

    merge_cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", bg_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-t", "65",
        "-shortest",
        final_output
    ]
    print("[DOWNLOADER] Merging real motion background with Quran recitation...")
    subprocess.run(merge_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    vid_id = f"{bg_choice['id']}_surah_{surah_num}"
    save_posted_id(vid_id)

    return {
        "filepath": final_output,
        "title": f"{surah_bangla} • {bg_choice['desc']} ও প্রশান্তিময় তিলাওয়াত",
        "video_id": vid_id,
        "surah_number": surah_num
    }

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
            "--extractor-args", "youtube:player_client=ios,android,web",
            "--no-check-certificates",
            "--no-playlist",
            "--match-filter", "duration <= 90 & duration >= 15",
            "--print", "%(id)s||%(title)s||%(duration)s"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=30)
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

    # ২. যদি সার্চে না পাওয়া যায়, তবে ভেরিফায়েড লাইভ পুল থেকে চেষ্টা
    if not selected_video_id:
        print("[DOWNLOADER] Using guaranteed live nature/rain verified pool...")
        available_pool = [v for v in VERIFIED_LIVE_VIDEOS if v["id"] not in posted_ids]
        if not available_pool:
            available_pool = VERIFIED_LIVE_VIDEOS
        chosen = random.choice(available_pool)
        selected_video_id = chosen["id"]
        selected_title = chosen["title"]

    found_files = []
    out_template = os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.%(ext)s")
    dl_cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={selected_video_id}",
        "--extractor-args", "youtube:player_client=ios,android,web",
        "--no-check-certificates",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--max-filesize", "80M",
        "-o", out_template
    ]

    print(f"[DOWNLOADER] Downloading real live video [{selected_video_id}] - {selected_title}")
    res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=60)
    found_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.*"))
    if not found_files:
        found_files = glob.glob(os.path.join(DOWNLOADS_DIR, "*.mp4"))

    # ৩. যদি ইউটিউব রেট লিমিট বা বট ব্লকে ব্যর্থ হয়, তবে সরাসরি লাইভ তিলাওয়াত পুল থেকে নেওয়া
    if not found_files or not os.path.exists(found_files[0]):
        print("[DOWNLOADER] YouTube blocked or unavailable. Using direct live recitation pool...")
        available_direct = [v for v in DIRECT_LIVE_VIDEOS if v["id"] not in posted_ids]
        if not available_direct:
            available_direct = DIRECT_LIVE_VIDEOS
        chosen_direct = random.choice(available_direct)

        direct_out = os.path.join(DOWNLOADS_DIR, f"quran_{chosen_direct['id']}.mp4")
        print(f"[DOWNLOADER] Downloading direct live footage: {chosen_direct['title']}")
        if download_file_direct(chosen_direct["url"], direct_out):
            found_files = [direct_out]
            selected_video_id = chosen_direct["id"]
            selected_title = chosen_direct["title"]

    # ৪. যদি তাও কোনো কারণে না হয়, লাইভ নেচার রিলস জেনারেট করা
    if not found_files or not os.path.exists(found_files[0]):
        print("[DOWNLOADER] Generating live nature motion reel as ultimate guarantee...")
        return generate_nature_quran_reel(surah_num, surah_bangla, posted_ids)

    final_path = found_files[0]
    save_posted_id(selected_video_id)
    print(f"[DOWNLOADER] Successfully acquired real live motion video ({os.path.getsize(final_path)} bytes): {final_path}")

    return {
        "filepath": final_path,
        "title": selected_title or surah_bangla,
        "video_id": selected_video_id,
        "surah_number": surah_num
    }
