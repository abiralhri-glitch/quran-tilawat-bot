"""
Holy Quran Automated Tilawat Engine & High-Retention Video Generator
- পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা ও মসজিদুল আকসার আসল ড্রোন ও সিনেমাটিক ফুটেজ
- মক্কা ও মদিনার সকল সম্মানিত ঐতিহাসিক ও বর্তমান ইমামগণের তিলাওয়াত
- পেজের স্থায়ী ব্র্যান্ডেড ওয়াটারমার্ক: 'কুরআনের তিলাওয়াত • Quran Tilawat'
- অ্যান্টি-কপিরাইট একোস্টিক ফিল্টারিং
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

from watermark_generator import generate_watermark_overlay
from quran_surah_database import MAKKAH_MADINAH_IMAMS, LONG_SURAHS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# স্থানীয় বাস্তব ফুটেজ তালিকা (মক্কা কা'বা, মদিনা মসজিদে নববী, আল-আকসা ও বৃষ্টি)
REAL_FOOTAGE_FILES = [
    "makkah_kaaba.mp4",
    "madinah_nabawi.mp4",
    "al_aqsa.mp4",
    "kaaba_rain.mp4"
]

def get_high_retention_video() -> str:
    """
    ১০০% আসল ও সিনেমাটিক মক্কা, মদিনা বা আল-আকসার ড্রোন ফুটেজ প্রদান করে।
    """
    available = []
    for f in REAL_FOOTAGE_FILES:
        p = os.path.join(ASSETS_FOOTAGE_DIR, f)
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            available.append(p)

    if available:
        chosen = random.choice(available)
        print(f"🎥 আসল সিনেমাটিক মসজিদ ফুটেজ লোড: {os.path.basename(chosen)} ({os.path.getsize(chosen)/(1024*1024):.2f} MB)")
        return chosen

    raise FileNotFoundError("কোনো আসল মসজিদ ফুটেজ পাওয়া যায়নি।")

def download_imam_surah_audio(surah_data: dict, imam: dict = None) -> tuple:
    """
    মক্কা ও মদিনার নির্দিষ্ট ইমামের ভেরিফাইড সিডিএন থেকে পূর্ণাঙ্গ সূরার অডিও সংগ্রহ করে।
    """
    surah_num = surah_data.get("number", 1)
    surah_bangla = surah_data.get("bangla", "সূরা আল-ফাতিহা")

    for old in glob.glob(os.path.join(DOWNLOADS_DIR, "voice_*.mp3")):
        try: os.remove(old)
        except Exception: pass

    if not imam:
        imam = random.choice(MAKKAH_MADINAH_IMAMS)

    print(f"🎙️ তিলাওয়াতকারী নির্বাচন: {imam['name']} ({imam['mosque']})")
    audio_path = os.path.join(DOWNLOADS_DIR, f"voice_{imam['id']}_{surah_num:03d}_{int(time.time())}.mp3")

    # ডিরেক্ট হাই-স্পিড সিডিএন ডাউনলোড (mp3quran.net)
    cdn_url = f"{imam['server']}/{surah_num:03d}.mp3"
    print(f"📥 অডিও ডাউনলোড হচ্ছে: {cdn_url}...")

    try:
        r = requests.get(cdn_url, stream=True, timeout=40, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        if r.status_code == 200:
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 30000:
                print(f"✅ সফল তিলাওয়াত অডিও ডাউনলোড: {os.path.getsize(audio_path)/(1024*1024):.2f} MB")
                return audio_path, imam
    except Exception as e:
        print(f"[IMAM CDN NOTICE] {e}")

    # ফলব্যাক: EveryAyah সিডিএন
    print(f"💡 ফলব্যাক EveryAyah সিডিএন থেকে {surah_bangla} সংগ্রহ হচ্ছে...")
    fallback_url = f"https://everyayah.com/data/Alafasy_128kbps/{surah_num:03d}001.mp3"
    try:
        r = requests.get(fallback_url, timeout=25)
        if r.status_code == 200:
            with open(audio_path, "wb") as f:
                f.write(r.content)
            return audio_path, {"id": "alafasy", "name": "শাইখ মিশারি রশিদ আল-আফাসি", "mosque": "গ্র্যান্ড মস্ক কুয়েত"}
    except Exception as e:
        print(f"[FALLBACK CDN ERROR] {e}")

    raise RuntimeError(f"অডিও তিলাওয়াত সংগ্রহ করা যায়নি: {surah_bangla}")

def render_quran_video_with_watermark(video_path: str, audio_path: str, out_path: str, is_reel: bool = True, max_duration: int = 58) -> str:
    """
    ভিডিওতে পেজের অফিশিয়াল ওয়াটারমার্ক সহ অ্যান্টি-কপিরাইট রেন্ডার সম্পন্ন করে:
    - ওয়াটারমার্ক: কুরআনের তিলাওয়াত • Quran Tilawat
    - ক্রপ ও স্কেলিং: 720x1280 (রিলস) বা 1280x720 (লং ভিডিও)
    - অ্যান্টি-কপিরাইট একোস্টিক ফিল্টার
    """
    print("🎨 পেজের অফিসিয়াল নিখুঁত ওয়াটারমার্ক সহ ভিডিও রেন্ডারিং শুরু...")

    if is_reel:
        w, h = 720, 1280
        video_scale = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
    else:
        w, h = 1280, 720
        video_scale = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720"

    watermark_png = generate_watermark_overlay(w, h)

    # একোস্টিক ফিল্টার ও ওয়াটারমার্ক ওভারলে
    audio_filter = "asetrate=48000*1.015,aresample=48000,atempo=0.985,bass=g=2:f=110,volume=1.05"
    filter_complex = f"[0:v]{video_scale}[scaled_v];[scaled_v][2:v]overlay=0:0[final_v]"

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", video_path,
        "-i", audio_path,
        "-i", watermark_png,
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "1:a:0",
        "-af", audio_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "21",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(max_duration),
        "-shortest",
        "-map_metadata", "-1",
        out_path
    ]

    subprocess.run(cmd, check=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"✨ রেন্ডারিং সম্পন্ন! সাইজ: {os.path.getsize(out_path)/(1024*1024):.2f} MB")
        return out_path
    else:
        raise RuntimeError("ভিডিও রেন্ডারিং সম্পন্ন হয়নি।")

def download_quran_video(search_query: str = None, is_reel: bool = True, surah_data: dict = None, imam_data: dict = None) -> dict:
    """quran_runner.py থেকে প্রধান এন্ট্রি পয়েন্ট"""
    if not surah_data:
        surah_data = random.choice(LONG_SURAHS)

    if not imam_data:
        imam_data = random.choice(MAKKAH_MADINAH_IMAMS)

    print("\n=======================================================")
    print(f"📖 'কুরআনের তিলাওয়াত' ভিডিও ইঞ্জিন: {surah_data['bangla']}")
    print(f"🎙️ তিলাওয়াত: {imam_data['name']} ({imam_data['mosque']})")
    print("=======================================================")

    bg_video = get_high_retention_video()
    voice_audio, imam = download_imam_surah_audio(surah_data, imam_data)

    ts = int(time.time())
    final_output = os.path.join(PROCESSED_DIR, f"quran_{surah_data['number']}_{ts}.mp4")

    duration = 58 if is_reel else 240
    render_quran_video_with_watermark(bg_video, voice_audio, final_output, is_reel=is_reel, max_duration=duration)

    # ক্লিনআপ টেম্প অডিও ফাইল
    try:
        if os.path.exists(voice_audio): os.remove(voice_audio)
    except Exception: pass

    return {
        "filepath": final_output,
        "file_path": final_output,
        "title": f"হৃদয় জুড়ানো তিলাওয়াত | {surah_data['bangla']} | {imam['name']}",
        "surah_name": surah_data["bangla"],
        "surah_number": surah_data["number"],
        "reciter": imam["name"],
        "mosque": imam["mosque"],
        "meaning": surah_data.get("meaning", ""),
        "benefit": surah_data.get("benefit", ""),
        "ayahs": surah_data.get("ayahs", "")
    }

if __name__ == "__main__":
    res = download_quran_video()
    print("ফলাফল:", res)
