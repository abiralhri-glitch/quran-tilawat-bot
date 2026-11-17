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
        "title": "মনোরম সবুজ অরণ্য ও প্রকৃতির স্নিগ্ধতা",
        "url": "https://archive.org/download/SlowLeaves/SlowLeavesH264.mp4"
    },
    {
        "id": "fern_waterfall_hd",
        "title": "পাহাড়ী ঝর্ণা ও শীতল জলপ্রপাত",
        "url": "https://archive.org/download/FernCreekFalls/FernCreekFalls-720_512kb.mp4"
    }
]

# আসল কুরআন মধুর তিলাওয়াত অডিও পুল - বহুমাত্রিক বিখ্যাত ক্বারীবৃন্দ (অ্যালগরিদম সুরক্ষা ও নিয়মিত রোটেশন)
HIGH_QUALITY_QURAN_AUDIO = [
    {
        "id": "audio_afs_055_rahman",
        "title": "سُورَةُ الرَّحْمَٰنِ • সূরা আর-রহমান",
        "reciter": "শাইখ মিশারি রশিদ আল-আফাসি",
        "url": "https://server8.mp3quran.net/afs/055.mp3"
    },
    {
        "id": "audio_sds_036_yasin",
        "title": "سُورَةُ يس • সূরা ইয়াসিন",
        "reciter": "শাইখ আব্দুর রহমান আস-সুদাইস",
        "url": "https://server11.mp3quran.net/sds/036.mp3"
    },
    {
        "id": "audio_gmd_056_waqiah",
        "title": "سُورَةُ الْوَاقِعَةِ • সূরা আল-ওয়াকিয়াহ",
        "reciter": "শাইখ সাদ আল-গামদি",
        "url": "https://server7.mp3quran.net/s_gmd/056.mp3"
    },
    {
        "id": "audio_shatr_020_taha",
        "title": "سُورَةُ طه • সূরা ত্বা-হা",
        "reciter": "শাইখ আবু বকর আশ-শাতরি",
        "url": "https://server11.mp3quran.net/shatr/020.mp3"
    },
    {
        "id": "audio_shur_018_kahf",
        "title": "سُورَةُ الْكَهْفِ • সূরা আল-কাহফ",
        "reciter": "শাইখ সাউদ আশ-শুরাইম",
        "url": "https://server7.mp3quran.net/shur/018.mp3"
    },
    {
        "id": "audio_sds_067_mulk",
        "title": "سُورَةُ الْمُلْكِ • সূরা আল-মুলক",
        "reciter": "শাইখ আব্দুর রহমান আস-সুদাইস",
        "url": "https://server11.mp3quran.net/sds/067.mp3"
    },
    {
        "id": "audio_afs_019_maryam",
        "title": "سُورَةُ مَرْيَمَ • সূরা মারিয়াম",
        "reciter": "শাইখ মিশারি রশিদ আল-আফাসি",
        "url": "https://server8.mp3quran.net/afs/019.mp3"
    },
    {
        "id": "audio_gmd_055_rahman",
        "title": "سُورَةُ الرَّحْمَٰনِ • সূরা আর-রহমান",
        "reciter": "শাইখ সাদ আল-গামদি",
        "url": "https://server7.mp3quran.net/s_gmd/055.mp3"
    },
    {
        "id": "audio_shatr_067_mulk",
        "title": "سُورَةُ الْمُلْكِ • সূরা আল-মুলক",
        "reciter": "শাইখ আবু বকর আশ-শাতরি",
        "url": "https://server11.mp3quran.net/shatr/067.mp3"
    },
    {
        "id": "audio_afs_056_waqiah",
        "title": "سُورَةُ الْوَاقِعَةِ • সূরা আল-ওয়াকিয়াহ",
        "reciter": "শাইখ মিশারি রশিদ আল-আফাসি",
        "url": "https://server8.mp3quran.net/afs/056.mp3"
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

def synthesize_live_nature_quran_video(surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (ঝর্ণা, বৃষ্টি, সবুজ অরণ্য) এবং বিশুদ্ধ কুরআন তিলাওয়াত অডিও একত্রিত করে 9:16 ফুলস্ক্রিন এইচডি রিলস তৈরি করে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    posted_ids = load_posted_ids()

    # Footage নির্বাচন
    available_footages = [f for f in LIVE_MOTION_FOOTAGE_POOL if f["id"] not in posted_ids]
    if not available_footages:
        available_footages = LIVE_MOTION_FOOTAGE_POOL
    selected_footage = random.choice(available_footages)

    # Audio নির্বাচন
    surah_num = surah_data.get("number", 0) if surah_data else 0
    audio_item = None
    if surah_num > 0:
        for a in HIGH_QUALITY_QURAN_AUDIO:
            if f"_{surah_num:03d}" in a["url"] or f"_{surah_num}_" in a["id"]:
                audio_item = a
                break

    if not audio_item:
        available_audios = [a for a in HIGH_QUALITY_QURAN_AUDIO if a["id"] not in posted_ids]
        if not available_audios:
            available_audios = HIGH_QUALITY_QURAN_AUDIO
        audio_item = random.choice(available_audios)

    print(f"[DOWNLOADER] Selected Live Motion Footage: {selected_footage['title']}")
    print(f"[DOWNLOADER] Selected Quran Recitation: {audio_item['title']} - {audio_item['reciter']}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    raw_video_path = None
    for attempt_footage in [selected_footage] + [f for f in LIVE_MOTION_FOOTAGE_POOL if f["id"] != selected_footage["id"]]:
        test_path = os.path.join(DOWNLOADS_DIR, f"raw_motion_{attempt_footage['id']}.mp4")
        if os.path.exists(test_path) and os.path.getsize(test_path) > 100000:
            raw_video_path = test_path
            selected_footage = attempt_footage
            break
        try:
            print(f"[DOWNLOADER] Downloading motion footage from: {attempt_footage['url']}")
            r_vid = requests.get(attempt_footage["url"], headers=headers, stream=True, timeout=60, allow_redirects=True)
            if r_vid.status_code == 200:
                with open(test_path, "wb") as f:
                    for chunk in r_vid.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                if os.path.getsize(test_path) > 100000:
                    raw_video_path = test_path
                    selected_footage = attempt_footage
                    break
        except Exception as e:
            print(f"[DOWNLOADER] Footage download notice ({attempt_footage['id']}): {e}")

    if not raw_video_path or not os.path.exists(raw_video_path):
        raise RuntimeError("Failed to download real live motion footage")

    # Download recitation audio
    raw_audio_path = os.path.join(DOWNLOADS_DIR, f"raw_audio_{surah_num}.mp3")
    try:
        print(f"[DOWNLOADER] Downloading recitation audio from: {audio_item['url']}")
        r_aud = requests.get(audio_item["url"], headers=headers, stream=True, timeout=60, allow_redirects=True)
        if r_aud.status_code == 200:
            with open(raw_audio_path, "wb") as f:
                for chunk in r_aud.iter_content(chunk_size=512 * 1024):
                    if chunk:
                        f.write(chunk)
    except Exception as e:
        print(f"[DOWNLOADER] Audio download error: {e}")

    if not os.path.exists(raw_audio_path) or os.path.getsize(raw_audio_path) < 10000:
        raise RuntimeError("Failed to download Quran recitation audio")

    # FFmpeg 9:16 Vertical Reel Synthesis
    # Explicitly map video from input 0 and recitation audio from input 1, with STRONGER anti-copyright audio filter
    out_id = f"{selected_footage['id']}_{audio_item['id']}_{int(time.time())}"
    final_output_path = os.path.join(DOWNLOADS_DIR, f"live_quran_{out_id}.mp4")
    target_duration = 50

    print(f"[DOWNLOADER] Synthesizing 9:16 vertical live motion reel via FFmpeg...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", raw_video_path,
        "-ss", "5",
        "-i", raw_audio_path,
        "-t", str(target_duration),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-af", "asetrate=44100*1.07,aresample=44100,atempo=0.935,volume=2.0,equalizer=f=300:width_type=o:width=2:g=4,equalizer=f=3000:width_type=o:width=2:g=-3,aecho=0.8:0.75:30:0.25",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output_path
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=180)
    if res.returncode == 0 and os.path.exists(final_output_path) and os.path.getsize(final_output_path) > 100000:
        print(f"[DOWNLOADER] Successfully synthesized live motion reel: {final_output_path}")
        save_posted_id(selected_footage["id"])
        save_posted_id(audio_item["id"])

        surah_title = audio_item["title"]
        reciter = audio_item["reciter"]
        nature_title = selected_footage["title"]
        full_title = f"{surah_title} • {nature_title} | ক্বারী {reciter}"

        return {
            "id": out_id,
            "filepath": final_output_path,
            "title": full_title,
            "description": f"📖 {surah_title}\n🌿 মনোরম প্রাকৃতিক দৃশ্য: {nature_title}\n🎙️ ক্বারী: {reciter}\n━━━━━━━━━━━━━━━━━━━━\nশান্ত ও স্নিগ্ধ কুরআন তিলাওয়াত অন্তরে প্রশান্তি বয়ে আনে। ❤️🤲\n\n#QuranTilawat #Nature #Rain #Surah #QuranRecitation #Peace",
            "source": "live_motion_engine",
            "duration": target_duration
        }
    else:
        print(f"[DOWNLOADER] FFmpeg synthesis error: {res.stderr[-300:]}")
        raise RuntimeError("FFmpeg live video rendering failed")

def download_quran_video(search_query: str, is_reel: bool = True, surah_data: dict = None) -> dict:
    """
    বাস্তব চলমান লাইভ ভিডিও (প্রকৃতি, বৃষ্টি, ঝর্ণা) ও বিশুদ্ধ কুরআন তিলাওয়াত রিলস নিশ্চিত করে।
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    # 1st Priority: Bulletproof Real Live Motion Synthesis Engine
    try:
        print(f"[DOWNLOADER] Initiating 100% Real Live Motion Video Engine for Quran Tilawat...")
        return synthesize_live_nature_quran_video(surah_data=surah_data)
    except Exception as e:
        print(f"[DOWNLOADER] Live motion synthesis notice: {e}, attempting online sources...")

    # Fallback to YouTube with anti-detection args
    surah_num = surah_data.get("number", 1) if surah_data else 1
    surah_bangla = surah_data.get("bangla", f"সূরা #{surah_num}") if surah_data else f"সূরা #{surah_num}"
    posted_ids = load_posted_ids()

    queries = [
        f"{surah_bangla} quran recitation nature rainfall shorts",
        f"{surah_bangla} তিলাওয়াত ড্রোন ভিডিও shorts",
        f"surah {surah_num} emotional beautiful recitation nature reels"
    ]

    for query in queries:
        print(f"[DOWNLOADER] Searching real live video for: {query}")
        search_cmd = [
            "yt-dlp",
            f"ytsearch8:{query}",
            "--get-id",
            "--get-title",
            "--get-duration",
            "--no-warnings",
            "--ignore-errors",
            "--extractor-args", "youtube:player_client=android,web"
        ]
        try:
            res = subprocess.run(search_cmd, capture_output=True, text=True, timeout=25)
            lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and "||" in l]
            for line in lines:
                parts = line.split("||")
                if len(parts) >= 2:
                    v_id = parts[0].strip()
                    v_title = parts[1].strip()
                    if v_id not in posted_ids:
                        target_file = os.path.join(DOWNLOADS_DIR, f"quran_{v_id}.mp4")
                        dl_cmd = [
                            "yt-dlp",
                            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                            "-o", target_file,
                            "--no-warnings",
                            "--ignore-errors",
                            "--extractor-args", "youtube:player_client=android,web",
                            f"https://www.youtube.com/watch?v={v_id}"
                        ]
                        subprocess.run(dl_cmd, capture_output=True, text=True, timeout=90)
                        if os.path.exists(target_file) and os.path.getsize(target_file) > 100000:
                            save_posted_id(v_id)
                            return {
                                "id": v_id,
                                "filepath": target_file,
                                "title": v_title,
                                "description": f"{v_title}\n\n#QuranTilawat #RealLiveVideo #Quran",
                                "source": "youtube",
                                "duration": 50
                            }
        except Exception as e:
            print(f"[DOWNLOADER] Search error: {e}")

    raise RuntimeError("Could not obtain a real moving Quran video.")
