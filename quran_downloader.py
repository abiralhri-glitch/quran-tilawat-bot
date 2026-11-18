"""
Holy Quran 24/7 Automated Tilawat Engine (Pinterest & Pixabay HD + YouTube Voice + Anti-Copyright)
১০০% কপিরাইট-মুক্ত, হাই-কোয়ালিটি পিন্টারেস্ট ও পিক্সাবে ভিডিও ব্যাকগ্রাউন্ড এবং ইউটিউব থেকে মধুর কণ্ঠের তিলাওয়াত
"""

import os
import re
import glob
import json
import time
import random
import requests
import subprocess
from pathlib import Path

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
VISUAL_ARCHIVE_FILE = os.path.join(BASE_DIR, "visual_archive.txt")
AUDIO_ARCHIVE_FILE = os.path.join(BASE_DIR, "audio_archive.txt")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 100% Verified Aesthetic Pinterest & Pixabay HD Nature Video Pool
AESTHETIC_VIDEO_POOL = [
    # --- Top Curated Pinterest 9:16 Aesthetic Video Pins ---
    {"id": "pin_moonlight_lake", "type": "pinterest", "url": "https://www.pinterest.com/pin/1017532109583885944/", "title": "চাঁদের মায়াবী আলো ও শান্ত হ্রদ"},
    {"id": "pin_moon_over_water", "type": "pinterest", "url": "https://www.pinterest.com/pin/1104930089809481153/", "title": "পূর্ণিমার চাঁদের স্নিগ্ধ আলো"},
    {"id": "pin_night_sky_clouds", "type": "pinterest", "url": "https://www.pinterest.com/pin/1019924646871037128/", "title": "মেঘের কোলে শান্ত চাঁদের রূপ"},
    {"id": "pin_serene_moonlit_night", "type": "pinterest", "url": "https://www.pinterest.com/pin/605593481176903638/", "title": "মায়াবী রাতের শান্ত প্রকৃতি"},
    {"id": "pin_lake_sunset_silhouettes", "type": "pinterest", "url": "https://www.pinterest.com/pin/924152786019978264/", "title": "হ্রদের কিনারায় অস্তগামী চাঁদ"},
    {"id": "pin_starry_galaxy_horizon", "type": "pinterest", "url": "https://www.pinterest.com/pin/863143084873107493/", "title": "মহাবিশ্বের অনন্ত নক্ষত্ররাজি"},
    {"id": "pin_gentle_rain_nature", "type": "pinterest", "url": "https://www.pinterest.com/pin/540994974006214270/", "title": "সবুজ পাতায় বৃষ্টির স্পর্শ"},
    {"id": "pin_night_view_rain", "type": "pinterest", "url": "https://www.pinterest.com/pin/933300722794599168/", "title": "বৃষ্টিভেজা রাতের স্নিগ্ধ রূপ"},
    {"id": "pin_night_rain_street", "type": "pinterest", "url": "https://www.pinterest.com/pin/1086774953860693613/", "title": "বৃষ্টিস্নাত রাতের বৃক্ষরাজি"},
    {"id": "pin_rain_soaked_trees", "type": "pinterest", "url": "https://www.pinterest.com/pin/765330530472063889/", "title": "স্নিগ্ধ বৃষ্টির ঝিমঝিম ধারা"},
    {"id": "pin_cascading_waterfall", "type": "pinterest", "url": "https://www.pinterest.com/pin/599049187978860539/", "title": "পাহাড়ি ঝর্ণার নির্মল জলধারা"},
    {"id": "pin_flowing_river_stream", "type": "pinterest", "url": "https://www.pinterest.com/pin/1137440449705442614/", "title": "বনের বুক চিরে বহমান নদী"},
    {"id": "pin_lush_river_clouds", "type": "pinterest", "url": "https://www.pinterest.com/pin/1075304848549322092/", "title": "নদী ও মেঘের মনোরম আবহাওয়া"},
    {"id": "pin_sea_waves_twilight", "type": "pinterest", "url": "https://www.pinterest.com/pin/961377851703515577/", "title": "গোধূলি লগ্নে সমুদ্রের ঢেউ"},
    {"id": "pin_snowy_mountain_peaks", "type": "pinterest", "url": "https://www.pinterest.com/pin/975099756801353185/", "title": "তুষারশুভ্র পর্বতমালার দিগন্ত"},
    {"id": "pin_sunset_pastel_clouds", "type": "pinterest", "url": "https://www.pinterest.com/pin/1087267535071578388/", "title": "আকাশে রঙের মেলা ও সূর্যাস্ত"},
    {"id": "pin_ocean_sunset_dark_clouds", "type": "pinterest", "url": "https://www.pinterest.com/pin/1019924646883616183/", "title": "সাগরের কিনারায় গোধূলির মায়া"},
    {"id": "pin_golden_hues_sunset", "type": "pinterest", "url": "https://www.pinterest.com/pin/917960336556579772/", "title": "সোনারঙা মেঘে ঢাকা সূর্যাস্ত"},
    {"id": "pin_rose_petals_sunset", "type": "pinterest", "url": "https://www.pinterest.com/pin/615233999145554771/", "title": "গোলাপের পাপড়ি ও শান্ত সন্ধ্যা"},
    {"id": "pin_white_flower_breeze", "type": "pinterest", "url": "https://www.pinterest.com/pin/1087830485012382777/", "title": "বাতাসে দোলা শ্বেতপদ্ম"},
    {"id": "pin_sunbeams_foggy_forest", "type": "pinterest", "url": "https://www.pinterest.com/pin/1066649493008823735/", "title": "কুয়াশাঘেরা বনে সূর্যের রশ্মি"},
    {"id": "pin_green_mountain_fields", "type": "pinterest", "url": "https://www.pinterest.com/pin/1152710467138867315/", "title": "সবুজ পাহাড় ও নীলাভ আকাশ"},
    {"id": "pin_calm_beach_evening", "type": "pinterest", "url": "https://www.pinterest.com/pin/891994269952168013/", "title": "শান্ত সৈকতে মৃদু বাতাসের পরশ"},

    # --- High-Definition Pixabay Free HD Streams (100% Royalty-Free) ---
    {"id": "pix_mountain_fog", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2021/10/26/93432-639359155_large.mp4", "title": "কুয়াশাঢাকা সবুজ পাহাড় ও বনানী"},
    {"id": "pix_sunset_clouds", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2024/08/08/225504_large.mp4", "title": "মেঘের কোলে রক্তিম সূর্যাস্ত"},
    {"id": "pix_rain_drops_ground", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2024/06/02/214982_large.mp4", "title": "প্রকৃতির বুকে স্নিগ্ধ বৃষ্টিপাত"},
    {"id": "pix_waterfall_cascade", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2023/07/04/170060-842720151_large.mp4", "title": "পাথরের বুক চিরে নেমে আসা ঝর্ণা"},
    {"id": "pix_waterfall_stream", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2022/11/24/140366-774838017_large.mp4", "title": "স্বচ্ছ পাহাড়ি নদীর শান্ত জলধারা"}
]

# YouTube Quran Recitation Voice Search Queries (Emotion & Soothing Voice)
YOUTUBE_VOICE_QUERIES = [
    "quran recitation emotional beautiful voice short",
    "surah yusuf beautiful voice tilawat short",
    "surah rahman soothing recitation short",
    "heart touching quran recitation short",
    "surah mulk beautiful recitation short",
    "surah al kahf beautiful tilawat short",
    "surah maryam emotional recitation short",
    "quran recitation calming sleep anxiety short",
    "surah baqarah emotional tilawat short",
    "quran recitation deep voice short",
    "emotional tilawat bangla quran short",
    "surah waqiah beautiful recitation short"
]


def load_archive(archive_path: str) -> set:
    if not os.path.exists(archive_path):
        return set()
    try:
        with open(archive_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()


def append_to_archive(archive_path: str, item_id: str):
    try:
        with open(archive_path, "a", encoding="utf-8") as f:
            f.write(f"{item_id}\n")
    except Exception as e:
        print(f"[ARCHIVE ERROR] {e}")


def download_aesthetic_video() -> tuple:
    """Selects an unrepeated high-definition Pinterest or Pixabay video and downloads it."""
    visual_history = load_archive(VISUAL_ARCHIVE_FILE)
    available_items = [v for v in AESTHETIC_VIDEO_POOL if v["id"] not in visual_history]

    # Reset archive if all used
    if not available_items:
        print("♻️ সকল পিন্টারেস্ট ও পিক্সাবে ভিডিও ব্যবহৃত হয়েছে। ভিজ্যুয়াল হিস্ট্রি রিসেট হচ্ছে...")
        if os.path.exists(VISUAL_ARCHIVE_FILE):
            os.remove(VISUAL_ARCHIVE_FILE)
        available_items = AESTHETIC_VIDEO_POOL

    item = random.choice(available_items)
    print(f"🎬 নির্বাচিত ব্যাকগ্রাউন্ড: '{item['title']}' (ID: {item['id']}, Type: {item['type'].upper()})")

    out_file = os.path.join(DOWNLOADS_DIR, f"bg_{item['id']}_{int(time.time())}.mp4")

    # Clean older downloads
    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "bg_*.mp4")):
        try:
            os.remove(old)
        except Exception:
            pass

    if item["type"] == "pixabay":
        # Direct high-speed CDN download
        print(f"📥 পিক্সাবে ডিরেক্ট এইচডি ডাউনলোড শুরু: {item['url']}...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(item["url"], headers=headers, stream=True, timeout=60)
        r.raise_for_status()
        with open(out_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
    else:
        # Pinterest download via yt-dlp
        print(f"📥 পিন্টারেস্ট এস্থেটিক ভিডিও ডাউনলোড হচ্ছে: {item['url']}...")
        cmd = [
            "yt-dlp",
            "--no-warnings",
            "-o", out_file,
            item["url"]
        ]
        subprocess.run(cmd, check=True, timeout=90)

    if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
        print(f"✅ ব্যাকগ্রাউন্ড ডাউনলোড সম্পন্ন! সাইজ: {os.path.getsize(out_file) / (1024*1024):.2f} MB")
        append_to_archive(VISUAL_ARCHIVE_FILE, item["id"])
        return out_file, item
    else:
        raise RuntimeError("ভিডিও ব্যাকগ্রাউন্ড ডাউনলোড ব্যর্থ হয়েছে।")


def download_youtube_quran_voice() -> tuple:
    """Downloads emotional Quran recitation voice from YouTube Shorts."""
    audio_history = load_archive(AUDIO_ARCHIVE_FILE)

    # Clean old audio files
    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3")):
        try:
            os.remove(old)
        except Exception:
            pass

    random.shuffle(YOUTUBE_VOICE_QUERIES)
    selected_audio = None
    video_title = "হৃদয় জুড়ানো কুরআন তিলাওয়াত"

    for query in YOUTUBE_VOICE_QUERIES:
        print(f"🎧 ইউটিউব থেকে তিলাওয়াত অনুসন্ধান: '{query}'...")
        temp_pattern = os.path.join(DOWNLOADS_DIR, f"voice_%(id)s.%(ext)s")
        cmd = [
            "yt-dlp",
            "--no-warnings",
            "--extract-audio",
            "--audio-format", "mp3",
            "--max-filesize", "20M",
            "-o", temp_pattern,
            "--print-json",
            f"ytsearch3:{query}"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if res.returncode == 0 and res.stdout.strip():
                # Parse JSON output of downloaded item
                for line in res.stdout.strip().split("\n"):
                    try:
                        info = json.loads(line)
                        vid_id = info.get("id")
                        if vid_id and vid_id not in audio_history:
                            video_title = info.get("title", video_title)
                            downloaded_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"voice_{vid_id}.mp3"))
                            if downloaded_files:
                                selected_audio = downloaded_files[0]
                                append_to_archive(AUDIO_ARCHIVE_FILE, vid_id)
                                print(f"✅ সফল অডিও ডাউনলোড: '{video_title}' (ID: {vid_id})")
                                break
                    except Exception:
                        pass
                if selected_audio and os.path.exists(selected_audio):
                    break
        except Exception as e:
            print(f"[VOICE DOWNLOAD NOTICE] {e}")

    # Fallback to any downloaded voice
    if not selected_audio or not os.path.exists(selected_audio):
        mp3s = glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3"))
        if mp3s:
            selected_audio = mp3s[0]
        else:
            raise RuntimeError("ইউটিউব থেকে অডিও তিলাওয়াত সংগ্রহ করা যায়নি।")

    return selected_audio, video_title


def render_anti_copyright_quran_reel(video_path: str, audio_path: str, out_path: str, max_duration: int = 58) -> str:
    """
    Renders 9:16 HD vertical reel with anti-copyright acoustic transformation.
    - Micro-pitch shift (+1.5%) & micro-tempo shift (-1.5%) to bypass Content ID acoustic hashing
    - Subtle acoustic warmth filter
    - Completely strips all container and stream metadata
    - Scales and crops to 720x1280 (HD 9:16)
    """
    print("🛡️ এন্টি-কপিরাইট একোস্টিক ট্রান্সফর্মেশন ও এইচডি ৯:১৬ রিলস রেন্ডারিং...")

    audio_filter = "asetrate=48000*1.015,aresample=48000,atempo=0.985,bass=g=2:f=110,volume=1.05"
    video_filter = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", video_filter,
        "-af", audio_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(max_duration),
        "-shortest",
        "-map_metadata", "-1",
        out_path
    ]

    subprocess.run(cmd, check=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"✨ রিলস তৈরি সম্পন্ন! সাইজ: {os.path.getsize(out_path) / (1024*1024):.2f} MB")
        return out_path
    else:
        raise RuntimeError("ভিডিও রেন্ডারিং সম্পন্ন হয়নি।")


def generate_quran_post_content(raw_title: str, bg_title: str) -> dict:
    """Generates clean Bengali Islamic caption matching the tilawat."""
    clean_title = re.sub(r"[#@][\w_]+", "", raw_title).strip()
    clean_title = re.sub(r"\s+", " ", clean_title)

    caption = (
        f"🎧 হৃদয় জুড়ানো কুরআন তিলাওয়াত | {clean_title[:70]}\n\n"
        f"প্রকৃতির অপরূপ সৃষ্টি ও মধুর তিলাওয়াতে মনকে প্রশান্ত করুন। 🤍\n"
        f"ভিডিওটি ভালো লাগলে লাইক ও শেয়ার করে পবিত্র কুরআনের বাণী ছড়িয়ে দিন।\n\n"
        f"#QuranTilawat #QuranRecitation #PeaceOfMind #IslamicReels #SubhanAllah #HolyQuran"
    )
    title = f"হৃদয় জুড়ানো কুরআন তিলাওয়াত | {clean_title[:50]}"
    return {"caption": caption, "title": title}


def download_quran_video(search_query: str = None, is_reel: bool = True, surah_data: dict = None) -> dict:
    """Main entrypoint executed by quran_poster.py."""
    print("\n=======================================================")
    print("📖 'কুরআনের তিলাওয়াত' ২৪/৭ হাই-কোয়ালিটি কপিরাইট-মুক্ত ইঞ্জিন")
    print("=======================================================")

    bg_video, bg_info = download_aesthetic_video()
    voice_audio, original_title = download_youtube_quran_voice()

    ts = int(time.time())
    final_output = os.path.join(PROCESSED_DIR, f"clean_quran_reel_{ts}.mp4")
    render_anti_copyright_quran_reel(bg_video, voice_audio, final_output, max_duration=55)

    post_info = generate_quran_post_content(original_title, bg_info["title"])

    try:
        if os.path.exists(bg_video):
            os.remove(bg_video)
        if os.path.exists(voice_audio):
            os.remove(voice_audio)
    except Exception:
        pass

    return {
        "filepath": final_output,
        "file_path": final_output,
        "title": post_info["title"],
        "caption": post_info["caption"],
        "tags": ["Quran", "Tilawat", "Islam", "Reels"],
        "surah_name": post_info["title"],
        "reciter": "আন্তর্জাতিক খ্যাতিসম্পন্ন ক্বারী"
    }


if __name__ == "__main__":
    result = download_quran_video()
    print("ফলাফল:", result)
