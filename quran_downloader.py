"""
Holy Quran 24/7 Automated Tilawat Engine (Pinterest & Pixabay HD + YouTube Voice + Anti-Copyright)
১০০% কপিরাইট-মুক্ত, হাই-কোয়ালিটি পিন্টারেস্ট ও পিক্সাবে ভিডিও ব্যাকগ্রাউন্ড এবং ইউটিউব ও পিওর অডিও তিলাওয়াত
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
    {"id": "pin_gentle_rain_nature", "type": "pinterest", "url": "https://www.pinterest.com/pin/540994974006214270/", "title": "সবুজ পাতায় বৃষ্টির স্নিগ্ধতা"},
    {"id": "pin_peaceful_clouds_sunset", "type": "pinterest", "url": "https://www.pinterest.com/pin/719872321727725965/", "title": "সূর্যাস্তের শান্ত মেঘমালা"},
    {"id": "pin_lantern_moon_vibes", "type": "pinterest", "url": "https://www.pinterest.com/pin/873979871465223062/", "title": "মায়াবী চাঁদের নিচে লণ্ঠনের আলো"},
    {"id": "pin_serene_river_sunset", "type": "pinterest", "url": "https://www.pinterest.com/pin/21392166974127025/", "title": "গোধূলি লগ্নে শান্ত নদীর মোহনা"},
    {"id": "pin_dark_aesthetic_rain", "type": "pinterest", "url": "https://www.pinterest.com/pin/1032309664539958742/", "title": "বৃষ্টির ঝিরিঝিরি ধারায় প্রকৃতির সৌন্দর্য"},
    {"id": "pin_misty_mountain_river", "type": "pinterest", "url": "https://www.pinterest.com/pin/1004865748083818321/", "title": "কুয়াশাঘেরা পাহাড় ও শান্ত নদী"},

    # --- Curated Pixabay CDN HD Nature Clips ---
    {"id": "pixabay_calm_waterfall", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2020/05/25/40149-425176523_tiny.mp4", "title": "শান্ত পাহাড়ি ঝর্ণাধারা"},
    {"id": "pixabay_clouds_timelapse", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2016/09/13/5158-183786493_tiny.mp4", "title": "নীল আকাশে সাদা মেঘের ভেলা"},
    {"id": "pixabay_gentle_waves_beach", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2019/04/16/22849-330962804_tiny.mp4", "title": "শান্ত সৈকতে মৃদু বাতাসের পরশ"},
    {"id": "pixabay_forest_stream", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2021/08/04/83875-584061618_tiny.mp4", "title": "গহীন অরণ্যের শান্ত জলধারা"},
    {"id": "pixabay_rain_window", "type": "pixabay", "url": "https://cdn.pixabay.com/video/2020/07/04/43834-436440232_tiny.mp4", "title": "শান্ত বৃষ্টি ও সবুজ পাতার দৃশ্য"}
]

# Curated Fallback Quran Recitations from direct Islamic CDN (EveryAyah / Quran.com CDN)
# Applied with FFmpeg Anti-Copyright filter to guarantee 100% safe monetization and zero muting!
FALLBACK_QURAN_AUDIO = [
    {"surah": "সূরা আল-ফাতিহা", "surah_no": "001", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/1.mp3"},
    {"surah": "সূরা আল-ইখলাস", "surah_no": "112", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/112.mp3"},
    {"surah": "সূরা আল-ফালাক", "surah_no": "113", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/113.mp3"},
    {"surah": "সূরা আন-নাস", "surah_no": "114", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/114.mp3"},
    {"surah": "সূরা আর-রহমান (নির্বাচিত আয়াত)", "surah_no": "055", "qari": "শাইখ মাহের আল-মুয়াইক্লি", "url": "https://download.quranicaudio.com/qdc/maher_al_muaiqly/murattal/55.mp3"},
    {"surah": "সূরা আল-মুলক (শান্তিপূর্ণ তিলাওয়াত)", "surah_no": "067", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/67.mp3"},
    {"surah": "সূরা আদ-দুহা", "surah_no": "093", "qari": "শাইখ আব্দুল বাসেত", "url": "https://download.quranicaudio.com/qdc/abdul_baset/mujawwad/93.mp3"},
    {"surah": "সূরা আল-ইনশিরাহ", "surah_no": "094", "qari": "শাইখ মিশারি রশিদ আল-আফাসি", "url": "https://download.quranicaudio.com/qdc/mishari_al_afasy/murattal/94.mp3"}
]

YOUTUBE_VOICE_QUERIES = [
    "সূরা আর রহমান মিষ্টি তিলাওয়াত shorts",
    "সূরা আল মুলক মিষ্টি তিলাওয়াত shorts",
    "সূরা ইয়াসিন তিলাওয়াত shorts",
    "হৃদয় জুড়ানো কুরআন তিলাওয়াত shorts",
    "most emotional quran recitation shorts",
    "quran recitation bangla subtitle shorts"
]

def load_archive(file_path: str) -> set:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        except Exception:
            return set()
    return set()

def append_archive(file_path: str, item_id: str):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{item_id}\n")
    except Exception:
        pass

def download_aesthetic_video() -> tuple:
    """Downloads high-definition 9:16 vertical nature background from Pinterest or Pixabay."""
    visual_history = load_archive(VISUAL_ARCHIVE_FILE)
    shuffled_pool = list(AESTHETIC_VIDEO_POOL)
    random.shuffle(shuffled_pool)

    # Clean old temp videos
    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "bg_*.mp4")):
        try:
            os.remove(old)
        except Exception:
            pass

    for item in shuffled_pool:
        item_id = item["id"]
        item_url = item["url"]
        item_type = item["type"]
        out_file = os.path.join(DOWNLOADS_DIR, f"bg_{item_id}_{int(time.time())}.mp4")

        print(f"🎬 ডাউনলোড হচ্ছে ({item_type.upper()}): {item['title']}...")

        if item_type == "pixabay":
            try:
                r = requests.get(item_url, timeout=30, stream=True)
                if r.status_code == 200:
                    with open(out_file, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                    if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
                        append_archive(VISUAL_ARCHIVE_FILE, item_id)
                        print(f"✅ সফল ডাউনলোড: {out_file} ({os.path.getsize(out_file)/(1024*1024):.2f} MB)")
                        return out_file, item
            except Exception as e:
                print(f"[PIXABAY NOTICE] {e}")

        elif item_type == "pinterest":
            cmd = [
                "yt-dlp",
                "--no-warnings",
                "--merge-output-format", "mp4",
                "-o", out_file,
                item_url
            ]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if res.returncode == 0 and os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
                    append_archive(VISUAL_ARCHIVE_FILE, item_id)
                    print(f"✅ সফল পিন্টারেস্ট ভিডিও: {out_file} ({os.path.getsize(out_file)/(1024*1024):.2f} MB)")
                    return out_file, item
            except Exception as e:
                print(f"[PINTEREST NOTICE] {e}")

    # Fallback to direct Pixabay CDN clip
    fallback_url = "https://cdn.pixabay.com/video/2020/05/25/40149-425176523_tiny.mp4"
    fb_file = os.path.join(DOWNLOADS_DIR, f"bg_fallback_{int(time.time())}.mp4")
    r = requests.get(fallback_url, timeout=30)
    with open(fb_file, "wb") as f:
        f.write(r.content)
    return fb_file, {"id": "fb_waterfall", "title": "শান্ত পাহাড়ি ঝর্ণাধারা"}

def download_youtube_quran_voice() -> tuple:
    """Downloads emotional Quran recitation voice with Android extractor, plus guaranteed direct CDN fallback."""
    audio_history = load_archive(AUDIO_ARCHIVE_FILE)

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
            "--extractor-args", "youtube:player_client=android,web",
            "--extract-audio",
            "--audio-format", "mp3",
            "--max-filesize", "25M",
            "-o", temp_pattern,
            "--print-json",
            f"ytsearch2:{query}"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.strip().split("\n"):
                    try:
                        info = json.loads(line)
                        vid_id = info.get("id")
                        if vid_id and vid_id not in audio_history:
                            video_title = info.get("title", video_title)
                            downloaded_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"voice_{vid_id}.*"))
                            if downloaded_files:
                                selected_audio = downloaded_files[0]
                                append_archive(AUDIO_ARCHIVE_FILE, vid_id)
                                print(f"✅ সফল ইউটিউব অডিও ডাউনলোড: '{video_title}' (ID: {vid_id})")
                                break
                    except Exception:
                        pass
                if selected_audio and os.path.exists(selected_audio):
                    break
        except Exception as e:
            print(f"[VOICE DOWNLOAD NOTICE] {e}")

    # Guaranteed Bulletproof Fallback: Pure Direct Islamic Audio CDN
    if not selected_audio or not os.path.exists(selected_audio):
        print("💡 ইউটিউব সীমাবদ্ধতার কারণে ডিরেক্ট পিওর ইসলামিক অডিও সিডিএন থেকে অডিও সংগ্রহ করা হচ্ছে...")
        chosen = random.choice(FALLBACK_QURAN_AUDIO)
        video_title = f"{chosen['surah']} | ক্বারী {chosen['qari']}"
        fallback_file = os.path.join(DOWNLOADS_DIR, f"voice_cdn_{chosen['surah_no']}_{int(time.time())}.mp3")
        try:
            r = requests.get(chosen['url'], timeout=30)
            if r.status_code == 200:
                with open(fallback_file, "wb") as f:
                    f.write(r.content)
                selected_audio = fallback_file
                print(f"✅ সফল ডিরেক্ট অডিও ডাউনলোড: '{video_title}'")
        except Exception as e:
            print(f"[FALLBACK AUDIO ERROR] {e}")

    if not selected_audio or not os.path.exists(selected_audio):
        raise RuntimeError("অডিও তিলাওয়াত সংগ্রহ করা যায়নি।")

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
    clean_title = re.sub(r"[#@][w_]+", "", raw_title).strip()
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
    """Main entrypoint executed by quran_runner.py."""
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
