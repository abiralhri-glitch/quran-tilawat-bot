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

# নিশ্চিত আসল চলমান লাইভ মোশন ব্যাকগ্রাউন্ড (ঝর্ণা, বৃষ্টি, সবুজ অরণ্য, পাহাড়) - 100% Verified Direct MP4
LIVE_MOTION_FOOTAGE_POOL = [
    {
        "id": "fern_waterfall_01",
        "title": "ঝর্ণার অপূর্ব জলধারা ও প্রশান্তিময় প্রকৃতি",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    },
    {
        "id": "rain_falling_01",
        "title": "বৃষ্টির শীতল স্পর্শ ও অন্তরের প্রশান্তি",
        "url": "https://archive.org/download/rain1932/Rain_512kb.mp4"
    },
    {
        "id": "slow_green_leaves_01",
        "title": "মনোরম সবুজ অরণ্য ও প্রকৃতির স্নিগ্ধ রূপ",
        "url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    },
    {
        "id": "fern_waterfall_hd",
        "title": "পাহাড়ী ঝর্ণার হৃদয়স্পর্শী বয়ে চলা জলধারা",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720.mp4"
    }
]

# মধুর কুরআন তিলাওয়াত অডিও সোর্স (বিশ্বখ্যাত ক্বারীগণ)
QURAN_AUDIO_POOLS = [
    {
        "surah_num": 36,
        "surah_name": "সূরা ইয়াসিন (سورة يس)",
        "reciter": "শাইখ আব্দুর রহমান আস-সুদাইস",
        "audio_url": "https://server11.mp3quran.net/sds/036.mp3"
    },
    {
        "surah_num": 55,
        "surah_name": "সূরা আর-রহমান (سورة الرحمن)",
        "reciter": "শাইখ মিশারি বিন রশিদ আল-আফাসি",
        "audio_url": "https://server8.mp3quran.net/afs/055.mp3"
    },
    {
        "surah_num": 56,
        "surah_name": "সূরা আল-ওয়াকিয়াহ (سورة الواقعة)",
        "reciter": "শাইখ সা'দ আল-গামদি",
        "audio_url": "https://server7.mp3quran.net/s_gmd/056.mp3"
    },
    {
        "surah_num": 67,
        "surah_name": "সূরা আল-মুলক (سورة الملك)",
        "reciter": "শাইখ মাহের আল-মুয়াইকিলি",
        "audio_url": "https://server12.mp3quran.net/maher/067.mp3"
    },
    {
        "surah_num": 18,
        "surah_name": "সূরা আল-কাহফ (سورة الكهف)",
        "reciter": "শাইখ সৌদ আশ-শুরাইম",
        "audio_url": "https://server7.mp3quran.net/shur/018.mp3"
    },
    {
        "surah_num": 25,
        "surah_name": "সূরা আল-ফুরকান (سورة الفرقان)",
        "reciter": "শাইখ ইয়াসির আদ-দুসারি",
        "audio_url": "https://server11.mp3quran.net/yasser/025.mp3"
    }
]

# ইউটিউব লাইভ ভিডিও রিলস পুল (fallback)
FALLBACK_YOUTUBE_VIDEOS = [
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

def synthesize_live_nature_quran_video(surah_data: dict = None) -> dict:
    """
    আসল লাইভ চলমান মোশন ভিডিও (ঝর্ণা/বৃষ্টি) + মধুর তিলাওয়াত অডিও সমন্বয় করে
    এফএফএমপেগের মাধ্যমে ৯:১৬ ফুল এইচডি ভিডিও তৈরি করে।
    """
    posted_ids = load_posted_ids()
    
    available_footages = [v for v in LIVE_MOTION_FOOTAGE_POOL if v["id"] not in posted_ids]
    if not available_footages:
        available_footages = list(LIVE_MOTION_FOOTAGE_POOL)
    
    random.shuffle(available_footages)
    
    available_audios = [a for a in QURAN_AUDIO_POOLS if f"audio_{a['surah_num']}" not in posted_ids]
    if not available_audios:
        available_audios = list(QURAN_AUDIO_POOLS)
    
    audio_meta = random.choice(available_audios)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # অডিও ডাউনলোড
    raw_audio_path = os.path.join(DOWNLOADS_DIR, f"raw_audio_{audio_meta['surah_num']}.mp3")
    if not os.path.exists(raw_audio_path) or os.path.getsize(raw_audio_path) < 10000:
        print(f"[DOWNLOADER] Downloading pure Quran audio recitation: {audio_meta['surah_name']}")
        r = requests.get(audio_meta["audio_url"], headers=headers, timeout=60, stream=True)
        r.raise_for_status()
        with open(raw_audio_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                f.write(chunk)

    # ফুটেজ লুপ ট্রাই
    for footage in available_footages:
        try:
            ts = int(time.time())
            raw_video_path = os.path.join(DOWNLOADS_DIR, f"raw_motion_{footage['id']}.mp4")
            final_output_path = os.path.join(DOWNLOADS_DIR, f"live_quran_{audio_meta['surah_num']}_{ts}.mp4")

            if not os.path.exists(raw_video_path) or os.path.getsize(raw_video_path) < 10000:
                print(f"[DOWNLOADER] Downloading real live footage from archive: {footage['title']}")
                r = requests.get(footage["url"], headers=headers, timeout=60, stream=True)
                r.raise_for_status()
                with open(raw_video_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        f.write(chunk)

            print(f"[DOWNLOADER] Rendering 9:16 Real Live Motion Quran Reel via FFmpeg...")
            target_duration = 55
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1",
                "-i", raw_video_path,
                "-ss", "10",
                "-i", raw_audio_path,
                "-t", str(target_duration),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                final_output_path
            ]
            
            proc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=180)
            if proc.returncode != 0 or not os.path.exists(final_output_path) or os.path.getsize(final_output_path) < 50000:
                raise RuntimeError(f"FFmpeg render error: {proc.stderr[:300]}")

            save_posted_id(footage["id"])
            save_posted_id(f"audio_{audio_meta['surah_num']}")

            title = f"{audio_meta['surah_name']} • {audio_meta['reciter']} • {footage['title']}"
            print(f"[DOWNLOADER] Live motion video successfully generated: {final_output_path}")

            return {
                "filepath": final_output_path,
                "video_path": final_output_path,
                "path": final_output_path,
                "title": title,
                "surah_name": audio_meta["surah_name"],
                "reciter": audio_meta["reciter"],
                "video_id": f"live_{footage['id']}_{ts}",
                "is_reel": True
            }
        except Exception as e:
            print(f"[DOWNLOADER] Footage {footage['title']} failed: {e}, trying next footage...")
            continue
            
    raise RuntimeError("Could not synthesize live video from any footage in pool.")

def download_from_youtube(video_id: str, title: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_tmpl = os.path.join(DOWNLOADS_DIR, f"yt_quran_{video_id}.%(ext)s")
    cmd = [
        "yt-dlp",
        "--extractor-args", "youtube:player_client=android,web",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--max-filesize", "90M",
        "-o", out_tmpl,
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if res.returncode == 0:
        matches = glob.glob(os.path.join(DOWNLOADS_DIR, f"yt_quran_{video_id}.*"))
        if matches and os.path.getsize(matches[0]) > 50000:
            final_p = matches[0]
            save_posted_id(video_id)
            return {
                "filepath": final_p,
                "video_path": final_p,
                "path": final_p,
                "title": title,
                "video_id": video_id,
                "is_reel": True
            }
    return None

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব লাইভ মোশন কুরআন তিলাওয়াত ভিডিও রিটার্ন করে।
    প্রথমেই নিশ্চিত লাইভ মোশন ব্যাকগ্রাউন্ড ও সুরমধুর তিলাওয়াত সিন্থেসাইজ করে।
    কোনো কারণে ফেইল করলে ইউটিউব লাইভ ভিডিও পুল ও সার্চ থেকে ডাউনলোড করে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    try:
        print("[DOWNLOADER] Initializing Real Live Motion Video Generation Pipeline...")
        result = synthesize_live_nature_quran_video(surah_data)
        if result and os.path.exists(result["filepath"]):
            return result
    except Exception as e:
        print(f"[DOWNLOADER] Synthesis fallback triggered due to: {e}")

    posted_ids = load_posted_ids()
    unposted_yt = [v for v in FALLBACK_YOUTUBE_VIDEOS if v["id"] not in posted_ids]
    if not unposted_yt:
        unposted_yt = FALLBACK_YOUTUBE_VIDEOS

    for v in unposted_yt:
        try:
            print(f"[DOWNLOADER] Trying verified live motion YouTube video: {v['title']}")
            res = download_from_youtube(v["id"], v["title"])
            if res:
                return res
        except Exception as e:
            print(f"[DOWNLOADER] YT error: {e}")

    # ফাইনাল সার্চ ফলব্যাক
    queries = [
        "quran recitation nature rain emotional 4k shorts",
        "beautiful quran recitation waterfall drone reels"
    ]
    for q in queries:
        try:
            search_cmd = [
                "yt-dlp",
                f"ytsearch5:{q}",
                "--extractor-args", "youtube:player_client=android,web",
                "--get-id",
                "--get-title"
            ]
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=25)
            lines = [l.strip() for l in res.stdout.strip().splitlines() if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                vid = parts[0].strip()
                vtitle = parts[1].strip() if len(parts) > 1 else "Holy Quran Tilawat"
                if vid and vid not in posted_ids:
                    down_res = download_from_youtube(vid, vtitle)
                    if down_res:
                        return down_res
        except Exception:
            pass

    raise RuntimeError("Could not obtain a real live motion Quran video from any source.")
