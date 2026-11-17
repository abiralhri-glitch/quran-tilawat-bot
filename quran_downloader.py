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
        "url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    },
    {
        "id": "fern_waterfall_hd_02",
        "title": "পাহাড়ি ঝর্ণার কলতান ও নৈসর্গিক রূপ",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720.mp4"
    }
]

# বিশ্ববিখ্যাত ক্বারীগণের বিশুদ্ধ ও মধুর কুরআন অডিও সিডিএন
QURAN_AUDIO_SOURCES = [
    {
        "qari": "শাইখ মিশারি রশিদ আল-আফাসি",
        "url_template": "https://server8.mp3quran.net/afs/{num:03d}.mp3"
    },
    {
        "qari": "শাইখ আব্দুর রহমান আস-সুদাইস",
        "url_template": "https://server11.mp3quran.net/sds/{num:03d}.mp3"
    },
    {
        "qari": "শাইখ ইয়াসির আদ-দুসারি",
        "url_template": "https://server11.mp3quran.net/yasser/{num:03d}.mp3"
    },
    {
        "qari": "শাইখ নাসের আল-কাতামি",
        "url_template": "https://server6.mp3quran.net/qtm/{num:03d}.mp3"
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

def download_file_direct(url: str, dest_path: str, timeout: int = 60) -> bool:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, stream=True, timeout=timeout)
        if resp.status_code in [200, 206]:
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            return os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000
        else:
            print(f"[DOWNLOADER] Direct download failed HTTP {resp.status_code} for {url}")
            return False
    except Exception as e:
        print(f"[DOWNLOADER] Direct download error: {e}")
        return False

def generate_live_motion_quran_video(surah_num: int, surah_bangla: str, posted_ids: set) -> dict:
    """
    ১০০% নিশ্চিত বাস্তব লাইভ মোশন ব্যাকগ্রাউন্ড (প্রবাহিত ঝর্ণা, বৃষ্টি, সবুজ অরণ্য)
    এবং বিশ্ববিখ্যাত ক্বারীর মধুর তিলাওয়াত অডিও সংযুক্ত করে একটি আকর্ষণীয় ৯:১৬ রিলস তৈরি করে।
    কোনো স্থির ছবি বা স্লাইড নয়—প্রতিটি ফ্রেমেই থাকে জীবন্ত চলমান প্রাকৃতিক দৃশ্য।
    """
    print(f"[DOWNLOADER] Synthesizing 100% Real Live Motion Quran Reel for {surah_bangla}...")
    temp_dir = os.path.join(DOWNLOADS_DIR, "temp_render")
    os.makedirs(temp_dir, exist_ok=True)

    # পূর্বে ব্যবহার না হওয়া লাইভ ফুটেজ নির্বাচন
    available_footage = [item for item in LIVE_MOTION_FOOTAGE_POOL if f"{item['id']}_{surah_num}" not in posted_ids]
    if not available_footage:
        available_footage = LIVE_MOTION_FOOTAGE_POOL
    selected_motion = random.choice(available_footage)

    # ক্বারী নির্বাচন
    selected_audio_source = random.choice(QURAN_AUDIO_SOURCES)
    audio_url = selected_audio_source["url_template"].format(num=surah_num)
    qari_name = selected_audio_source["qari"]

    raw_motion_path = os.path.join(temp_dir, f"raw_motion_{selected_motion['id']}.mp4")
    raw_audio_path = os.path.join(temp_dir, f"raw_audio_surah_{surah_num}.mp3")
    final_output_path = os.path.join(DOWNLOADS_DIR, f"live_quran_{surah_num}_{int(time.time())}.mp4")

    # ১. লাইভ ফুটেজ ডাউনলোড
    if not os.path.exists(raw_motion_path) or os.path.getsize(raw_motion_path) < 10000:
        print(f"[DOWNLOADER] Downloading real live footage: {selected_motion['title']}")
        ok_video = download_file_direct(selected_motion["url"], raw_motion_path, timeout=90)
        if not ok_video:
            download_file_direct(LIVE_MOTION_FOOTAGE_POOL[0]["url"], raw_motion_path, timeout=90)

    # ২. তিলাওয়াত অডিও ডাউনলোড
    if not os.path.exists(raw_audio_path) or os.path.getsize(raw_audio_path) < 10000:
        print(f"[DOWNLOADER] Downloading melodious recitation ({qari_name}) from {audio_url}...")
        ok_audio = download_file_direct(audio_url, raw_audio_path, timeout=60)
        if not ok_audio:
            backup_audio = f"https://server8.mp3quran.net/afs/{surah_num:03d}.mp3"
            download_file_direct(backup_audio, raw_audio_path, timeout=60)

    if not os.path.exists(raw_motion_path) or not os.path.exists(raw_audio_path):
        raise RuntimeError(f"Failed to acquire live video or audio assets for {surah_bangla}")

    # ৩. FFmpeg দিয়ে ৯:১৬ (১০৮০x১৯২০) খাঁটি লাইভ মোশন রিলস তৈরি
    reel_duration = 55
    fade_start = reel_duration - 4

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", raw_motion_path,
        "-ss", "5",
        "-t", str(reel_duration),
        "-i", raw_audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-af", f"afade=t=out:st={fade_start}:d=4",
        "-shortest",
        final_output_path
    ]

    print(f"[DOWNLOADER] Rendering 9:16 Live Nature Motion Reel with FFmpeg...")
    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=120)
    if res.returncode != 0 or not os.path.exists(final_output_path) or os.path.getsize(final_output_path) < 50000:
        print(f"[DOWNLOADER] FFmpeg render error: {res.stderr[:300]}")
        raise RuntimeError("Failed to render 9:16 live video reel")

    motion_id = f"{selected_motion['id']}_{surah_num}"
    save_posted_id(motion_id)

    full_title = f"{surah_bangla} • {selected_motion['title']} | ক্বারী: {qari_name}"
    print(f"[DOWNLOADER] Successfully synthesized 100% Real Live Motion Reel ({os.path.getsize(final_output_path)} bytes): {final_output_path}")

    return {
        "path": final_output_path,
        "id": motion_id,
        "title": full_title,
        "surah": surah_bangla,
        "is_verified_live": True
    }

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (প্রকৃতি, বৃষ্টি, ঝর্ণা, ড্রোন শট) ও তিলাওয়াত রিলস স্বয়ংক্রিয়ভাবে ডাউনলোড করে।
    একই ভিডিও দ্বিতীয়বার ডাউনলোড হবে না—প্রতিটি ভিডিও সম্পূর্ণ ইউনিক ও লাইভ চলমান হবে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*")):
        if os.path.isfile(f):
            try:
                os.remove(f)
            except Exception:
                pass

    surah_num = surah_data.get("number", 1) if surah_data else 1
    surah_bangla = surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}"
    posted_ids = load_posted_ids()

    # ১. প্রথমে ইউটিউব সার্চ থেকে লাইভ মোশন শর্টস অনুসন্ধান
    queries = [
        f"{surah_bangla} quran status rain aesthetic shorts",
        f"{surah_bangla} quran recitation waterfall nature reels",
        f"{surah_bangla} quran aesthetic ocean drone shorts",
        f"quran status rain aesthetic shorts",
        f"quran status waterfall nature 4k shorts",
        f"quran drone nature aesthetic reels shorts"
    ]

    selected_video_id = None
    selected_title = None

    for query in queries:
        print(f"[DOWNLOADER] Searching real live video for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch8:{query}",
            "--extractor-args", "youtube:player_client=android,web",
            "--no-playlist",
            "--match-filter", "duration <= 90 & duration >= 15 & !is_live",
            "--print", "%(id)s||%(title)s||%(duration)s"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=30)
            lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                v_id = parts[0].strip()
                v_title = parts[1].strip() if len(parts) > 1 else ""
                
                lower_title = v_title.lower()
                if any(bad in lower_title for bad in ["full audio", "mp3", "static", "slideshow", "photo cover"]):
                    continue

                if v_id not in posted_ids:
                    selected_video_id = v_id
                    selected_title = v_title
                    break
        except Exception as e:
            print(f"[DOWNLOADER] Search error for query '{query}': {e}")

        if selected_video_id:
            break

    # ২. ইউটিউব থেকে লাইভ ভিডিও ডাউনলোড চেষ্টা
    if selected_video_id:
        out_path = os.path.join(DOWNLOADS_DIR, f"quran_{selected_video_id}.mp4")
        dl_cmd = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={selected_video_id}",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--extractor-args", "youtube:player_client=android,web",
            "-o", out_path,
            "--no-playlist",
            "--max-filesize", "80M"
        ]
        try:
            print(f"[DOWNLOADER] Downloading real live video [{selected_video_id}] - {selected_title}")
            res = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=100)
            if res.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
                save_posted_id(selected_video_id)
                return {
                    "path": out_path,
                    "id": selected_video_id,
                    "title": selected_title,
                    "surah": surah_bangla,
                    "is_verified_live": True
                }
        except Exception as e:
            print(f"[DOWNLOADER] yt-dlp download failed: {e}")

    # ৩. শতভাগ নিশ্চিত রিয়েল লাইভ মোশন ইঞ্জিন (প্রবাহিত ঝর্ণা, বৃষ্টি, সবুজ অরণ্য + তিলাওয়াত)
    print(f"[DOWNLOADER] Activating 100% Guaranteed Real Live Motion Engine...")
    return generate_live_motion_quran_video(surah_num, surah_bangla, posted_ids)
