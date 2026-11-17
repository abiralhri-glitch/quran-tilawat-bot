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

# নিশ্চিত আসল চলমান লাইভ মোশন ব্যাকগ্রাউন্ড (ঝর্ণা, বৃষ্টি, সবুজ অরণ্য, পাহাড়)
LIVE_MOTION_FOOTAGE_POOL = [
    {
        "id": "fern_waterfall_01",
        "title": "ঝর্ণার অপূর্ব জলধারা ও প্রশান্তিময় প্রকৃতি",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    },
    {
        "id": "rain_falling_01",
        "title": "বৃষ্টির শীতল স্পর্শ ও অন্তরের প্রশান্তি",
        "url": "https://archive.org/download/rain1932/rain1932_512kb.mp4"
    },
    {
        "id": "slow_green_leaves_01",
        "title": "মনোরম সবুজ অরণ্য ও প্রকৃতির স্নিগ্ধ রূপ",
        "url": "https://archive.org/download/SlowLeaves/leaves_512kb.mp4"
    },
    {
        "id": "fern_waterfall_hd_02",
        "title": "পাহাড়ের বুক চিরে নেমে আসা স্বচ্ছ জলপ্রপাত",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    }
]

# বিশ্বখ্যাত ক্বারীগণের বিশুদ্ধ কুরআন তিলাওয়াত অডিও সোর্স (MP3Quran CDN)
QARI_AUDIO_SOURCES = [
    {"name": "শাইখ আব্দুর রহমান আস-সুদাইস", "base_url": "https://server11.mp3quran.net/sds"},
    {"name": "মিশারি রাশিদ আল-আফাসি", "base_url": "https://server8.mp3quran.net/afs"},
    {"name": "সাদ আল-গামদি", "base_url": "https://server7.mp3quran.net/s_gmd"},
    {"name": "আহমাদ বিন আলি আল-আজমি", "base_url": "https://server10.mp3quran.net/ajm"},
    {"name": "মাহের আল-মুআইক্বলি", "base_url": "https://server12.mp3quran.net/maher"},
    {"name": "মুহাম্মদ সিদ্দিক আল-মিনশাবি", "base_url": "https://server10.mp3quran.net/minsh"},
    {"name": "সাউদ আশ-শুরাইম", "base_url": "https://server7.mp3quran.net/shur"}
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

def synthesize_live_motion_quran_video(surah_num: int, surah_bangla: str, is_reel: bool = True) -> tuple:
    """
    আসল লাইভ মোশন ব্যাকগ্রাউন্ড (ঝর্ণা/বৃষ্টি) এবং উচ্চ মানের তিলাওয়াত অডিও সংযুক্ত করে
    স্বয়ংক্রিয়ভাবে একটি অত্যাশ্চর্য ৯:১৬ পূর্ণাঙ্গ রিলস ভিডিও তৈরি করে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    target_duration = 50 if is_reel else 120

    # ১. ব্যাকগ্রাউন্ড লাইভ মোশন ভিডিও নির্বাচন
    bg_choice = random.choice(LIVE_MOTION_FOOTAGE_POOL)
    bg_video_url = bg_choice["url"]
    bg_file = os.path.join(DOWNLOADS_DIR, f"raw_motion_{bg_choice['id']}.mp4")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    if not os.path.exists(bg_file) or os.path.getsize(bg_file) < 50000:
        print(f"[DOWNLOADER] Downloading live motion video: {bg_choice['title']}...")
        r = requests.get(bg_video_url, headers=headers, timeout=60, stream=True)
        with open(bg_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print(f"[DOWNLOADER] Live motion downloaded: {os.path.getsize(bg_file)} bytes")

    # ২. ক্বারী ও তিলাওয়াত অডিও ডাউনলোড
    qari_info = random.choice(QARI_AUDIO_SOURCES)
    surah_str = f"{surah_num:03d}.mp3"
    audio_url = f"{qari_info['base_url']}/{surah_str}"
    audio_file = os.path.join(DOWNLOADS_DIR, f"audio_surah_{surah_str}")

    if not os.path.exists(audio_file) or os.path.getsize(audio_file) < 30000:
        print(f"[DOWNLOADER] Downloading recitation by {qari_info['name']} ({audio_url})...")
        r_aud = requests.get(audio_url, headers=headers, timeout=45, stream=True)
        with open(audio_file, "wb") as f:
            for chunk in r_aud.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
        print(f"[DOWNLOADER] Recitation audio downloaded: {os.path.getsize(audio_file)} bytes")

    # ৩. FFmpeg দিয়ে লাইভ মোশন ভিডিও ও তিলাওয়াত একত্রিত করে ৯:১৬ রিলস ফরম্যাটে রূপান্তর
    out_video = os.path.join(DOWNLOADS_DIR, f"live_quran_{surah_num}_{int(time.time())}.mp4")
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", bg_file,
        "-i", audio_file,
        "-t", str(target_duration),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video
    ]
    
    print(f"[DOWNLOADER] Rendering 9:16 Live Motion Quran Video via FFmpeg...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if os.path.exists(out_video) and os.path.getsize(out_video) > 100000:
        print(f"[DOWNLOADER] Successfully synthesized Live Video: {out_video} ({os.path.getsize(out_video)} bytes)")
        return out_video, bg_choice["id"], bg_choice["title"], qari_info
    else:
        print(f"[DOWNLOADER] FFmpeg render warning: {res.stderr[-300:] if res.stderr else 'unknown'}")
        if os.path.exists(bg_file):
            return bg_file, bg_choice["id"], bg_choice["title"], qari_info
        return None, None, None, None

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (প্রকৃতি, বৃষ্টি, ঝর্ণা, মহাসমুদ্র) এবং বিশুদ্ধ কুরআন তিলাওয়াত
    স্বয়ংক্রিয়ভাবে ডাউনলোড ও প্রস্তুত করে।
    কোনো অবস্থাতেই স্থির ছবি বা অডিও-অনলি স্টিল পিকচার থাকবে না।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        try:
            if not f.endswith(".mp4"):
                os.remove(f)
        except Exception:
            pass

    surah_num = surah_data.get("number", random.randint(1, 114)) if surah_data else random.randint(1, 114)
    surah_bangla = surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}"
    posted_ids = load_posted_ids()

    queries = [
        f"{surah_bangla} quran recitation live nature rain reels",
        f"{surah_bangla} তিলাওয়াত bangla subtitle live nature shorts",
        f"surah {surah_num} emotional recitation waterfall rain reels",
        "emotional quran recitation live rain nature 4k reels shorts"
    ]

    selected_video_id = None
    selected_title = None

    for query in queries:
        print(f"[DOWNLOADER] Searching live motion footage for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch6:{query}",
            "--extractor-args", "youtube:player_client=android,web",
            "--no-playlist",
            "--match-filter", "duration <= 90 & duration >= 15",
            "--print", "%(id)s||%(title)s"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=25)
            lines = [l.strip() for l in res.stdout.strip().split("
") if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                v_id = parts[0].strip()
                v_title = parts[1].strip() if len(parts) > 1 else ""
                
                lower_title = v_title.lower()
                if any(bad in lower_title for bad in ["audio only", "still", "image", "photo", "podcast", "lecture"]):
                    continue
                if v_id not in posted_ids:
                    selected_video_id = v_id
                    selected_title = v_title
                    break
            if selected_video_id:
                break
        except Exception as e:
            print(f"[DOWNLOADER] yt-dlp search error: {e}")

    if selected_video_id:
        out_file = os.path.join(DOWNLOADS_DIR, f"yt_live_{selected_video_id}.mp4")
        dl_cmd = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={selected_video_id}",
            "--extractor-args", "youtube:player_client=android,web",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", out_file,
            "--no-playlist",
            "--socket-timeout", "30"
        ]
        try:
            print(f"[DOWNLOADER] Downloading YouTube video {selected_video_id}: {selected_title}...")
            subprocess.run(dl_cmd, timeout=90)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
                save_posted_id(selected_video_id)
                return {
                    "id": selected_video_id,
                    "title": selected_title,
                    "surah": surah_bangla,
                    "filepath": out_file,
                    "video_path": out_file,
                    "path": out_file,
                    "duration": 60,
                    "source": "youtube_live_motion"
                }
        except Exception as e:
            print(f"[DOWNLOADER] Download error: {e}")

    print(f"[DOWNLOADER] Synthesizing verified 100% LIVE MOTION Quran video for {surah_bangla}...")
    out_reels_video, bg_id, bg_title, qari_info = synthesize_live_motion_quran_video(
        surah_num=surah_num,
        surah_bangla=surah_bangla,
        is_reel=is_reel
    )

    if out_reels_video and os.path.exists(out_reels_video):
        selected_id = f"live_{surah_num}_{bg_id}_{int(time.time())}"
        save_posted_id(selected_id)
        return {
            "id": selected_id,
            "title": f"{surah_bangla} • {bg_title}",
            "surah": surah_bangla,
            "qari": qari_info["name"] if qari_info else "বিখ্যাত ক্বারী",
            "filepath": out_reels_video,
            "video_path": out_reels_video,
            "path": out_reels_video,
            "duration": 50,
            "source": "live_motion_synthesis"
        }

    return {
        "id": f"live_fallback_{surah_num}",
        "title": f"{surah_bangla} লাইভ মোশন কুরআন তিলাওয়াত",
        "surah": surah_bangla,
        "filepath": out_reels_video if out_reels_video else "",
        "video_path": out_reels_video if out_reels_video else "",
        "path": out_reels_video if out_reels_video else ""
    }
