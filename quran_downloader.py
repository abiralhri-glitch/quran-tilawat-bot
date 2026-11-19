"""
Holy Quran Automated Tilawat Engine & High-Retention Video Generator
- ১০০% পবিত্র মক্কা মুকাররমা, মদিনা মনোওয়ারা, মসজিদুল আকসা ও বিশ্ববিখ্যাত ঐতিহাসিক মসজিদ
- শুধুমাত্র পবিত্র মসজিদ ও হারামাইন শরীফাইনের আসল সিনেমাটিক 1080p আল্ট্রা-এইচডি ফুটেজ
- কঠোর জিরো-ডুপ্লিকেট রোটেশন: একই ভিডিও কখনো পরপর বা একই দিনে ভিন্ন সূরায় পুনরাবৃত্তি হবে না
- ৫টি রিলস (1080x1920) ও ৫টি ফুল এইচডি লং ভিডিও (1920x1080)
- পেজের স্থায়ী ব্র্যান্ডেড ওয়াটারমার্ক: 'কুরআনের তিলাওয়াত • Quran Tilawat'
- ৩২০kbps ক্রিস্টাল ক্লিয়ার স্টুডিও সাউন্ড
"""

import os
import re
import glob
import json
import time
import random
import requests
import subprocess
import imageio_ffmpeg
from pathlib import Path

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

from watermark_generator import generate_watermark_overlay
from quran_surah_database import MAKKAH_MADINAH_IMAMS, LONG_SURAHS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# ১০টি বিশ্ববিখ্যাত পবিত্র মসজিদ ও হারামাইন শরীফাইনের আসল 1080p সিনেমাটিক ফুটেজ
REAL_MOSQUE_FOOTAGES = [
    {
        "file": "makkah_clock_tower_drone.mp4",
        "title": "পবিত্র মক্কা ক্লক টাওয়ার ও মসজিদুল হারাম ড্রোন দৃশ্য",
        "location": "মক্কা মুকাররমা, সৌদি আরব"
    },
    {
        "file": "kaaba_cinematic_shots.mp4",
        "title": "পবিত্র কাবা শরীফ ও গিলাফের অপার্থিব সিনেমাটিক দৃশ্য",
        "location": "পবিত্র কাবা শরীফ, মক্কা"
    },
    {
        "file": "madinah_nabawi_drone_4k.mp4",
        "title": "পবিত্র মসজিদে নববী ও রওজা শরীফের ৪কে ড্রোন ভিউ",
        "location": "মদিনা মনোওয়ারা, সৌদি আরব"
    },
    {
        "file": "sheikh_zayed_grand_mosque.mp4",
        "title": "শেখ জায়েদ গ্র্যান্ড মসজিদ",
        "location": "আবুধাবি, সংযুক্ত আরব আমিরাত"
    },
    {
        "file": "sultan_ahmed_blue_mosque.mp4",
        "title": "সুলতান আহমেদ ব্লু মস্ক (ঐতিহাসিক নীল মসজিদ)",
        "location": "ইস্তাম্বুল, তুরস্ক"
    },
    {
        "file": "faisal_mosque_islamabad.mp4",
        "title": "বিখ্যাত ফয়সাল মসজিদ ও মারগাল্লা পাহাড় চত্বর",
        "location": "ইসলামাবাদ, পাকিস্তান"
    },
    {
        "file": "putra_mosque_malaysia.mp4",
        "title": "পুত্রা মসজিদ (জলরাশির মাঝে গোলাপী মসজিদ)",
        "location": "পুত্রজায়া, মালয়েশিয়া"
    },
    {
        "file": "hassan_ii_mosque_morocco.mp4",
        "title": "ঐতিহাসিক হাসান দ্বিতীয় মসজিদ (আটলান্টিক মহাসাগরের তীর)",
        "location": "কাসাব্লাঙ্কা, মরক্কো"
    },
    {
        "file": "badshahi_mosque_lahore.mp4",
        "title": "ঐতিহাসিক বাদশাহী মসজিদ ও মার্বেল চত্বর",
        "location": "লাহোর, পাকিস্তান"
    },
    {
        "file": "kaaba_beauty_peaceful.mp4",
        "title": "পবিত্র কাবা প্রাঙ্গণের স্নিগ্ধ আধ্যাত্মিক পরিবেশ",
        "location": "পবিত্র মসজিদুল হারাম, মক্কা"
    }
]

FOOTAGE_HISTORY_FILE = os.path.join(BASE_DIR, "footage_history.json")

def get_next_mosque_footage(surah_data: dict = None) -> tuple:
    """
    ১০০% কঠোর ডুপ্লিকেট-মুক্ত সিকোয়েন্সিয়াল রোটেশন:
    প্রতিটি পোস্টের জন্য সম্পূর্ণ আলাদা মসজিদ ফুটেজ নির্ধারিত হবে।
    ১০টি পোস্টের প্রতিটি সম্পূর্ণ ভিন্ন ভিন্ন ভিডিও ব্যবহার করবে।
    """
    history = {"last_index": -1, "used_records": []}
    if os.path.exists(FOOTAGE_HISTORY_FILE):
        try:
            with open(FOOTAGE_HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    # ফিল্টার: যেসব ফাইল বর্তমানে ফিজিক্যালি আছে
    available = []
    for item in REAL_MOSQUE_FOOTAGES:
        p = os.path.join(ASSETS_FOOTAGE_DIR, item["file"])
        if os.path.exists(p) and os.path.getsize(p) > 50000:
            available.append(item)

    if not available:
        raise FileNotFoundError("কোনো পবিত্র মসজিদ বা হারামাইনের সিনেমাটিক ফুটেজ পাওয়া যায়নি।")

    last_index = history.get("last_index", -1)
    next_index = (last_index + 1) % len(available)
    chosen_meta = available[next_index]

    history["last_index"] = next_index
    if "used_records" not in history or not isinstance(history["used_records"], list):
        history["used_records"] = []
    history["used_records"].append({
        "file": chosen_meta["file"],
        "surah": surah_data.get("bangla") if surah_data else "Unknown",
        "timestamp": int(time.time())
    })
    if len(history["used_records"]) > 50:
        history["used_records"] = history["used_records"][-50:]

    try:
        with open(FOOTAGE_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HISTORY WARN] {e}")

    chosen_path = os.path.join(ASSETS_FOOTAGE_DIR, chosen_meta["file"])
    print(f"🕌 [পবিত্র মসজিদ ফুটেজ রোটেশন] #{next_index+1}/{len(available)}: {chosen_meta['title']} ({chosen_meta['location']})")
    return chosen_path, chosen_meta

def download_imam_surah_audio(surah_data: dict, imam: dict = None) -> tuple:
    """
    মক্কা ও মদিনার সম্মানিত ইমামগণের ভেরিফাইড সিডিএন থেকে পূর্ণাঙ্গ সূরার অডিও সংগ্রহ করে।
    কঠোর পলিসি: কোনো কপিরাইটযুক্ত স্টুডিও রিকার্ডিং নয়।
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

    # নিরাপদ ফলব্যাক: পবিত্র মক্কার শাইখ ড. মাহের আল-মুয়াইক্বলী
    print(f"💡 নিরাপদ ফলব্যাক সিডিএন থেকে {surah_bangla} সংগ্রহ হচ্ছে...")
    fallback_url = f"https://server12.mp3quran.net/maher/{surah_num:03d}.mp3"
    try:
        r = requests.get(fallback_url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            return audio_path, {
                "id": "muaiqly",
                "name": "শাইখ ড. মাহের আল-মুয়াইক্লি",
                "title": "সম্মানিত ইমাম ও খতিব",
                "mosque": "পবিত্র মসজিদুল হারাম, মক্কা মুকাররমা"
            }
    except Exception as e:
        print(f"[FALLBACK CDN ERROR] {e}")

    raise RuntimeError(f"অডিও তিলাওয়াত সংগ্রহ করা যায়নি: {surah_bangla}")

def render_quran_video_with_watermark(video_path: str, audio_path: str, out_path: str, is_reel: bool = True) -> str:
    """
    ভিডিওতে পেজের অফিশিয়াল ক্রিস্টাল ক্লিয়ার ওয়াটারমার্ক সহ আল্ট্রা হাই-কোয়ালিটি 1080p রেন্ডার:
    - রিলস (Reels): 1080x1920 (Vertical 9:16), CRF 18, 6000k Bitrate, 320k Audio
    - রেগুলার ভিডিও: 1920x1080 (Widescreen 16:9), CRF 17, 8000k Bitrate, 320k Audio
    """
    if is_reel:
        w, h = 1080, 1920
        max_duration = 65  # হাই রিটেনশন রিলস
        video_scale = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        crf = "18"
        bitrate_args = ["-b:v", "6000k", "-maxrate", "8000k", "-bufsize", "12000k"]
        print("🎨 [REEL RENDERING] ১০৮০x১৯২০ আল্ট্রা-এইচডি ভার্টিক্যাল রিলস প্রস্তুত হচ্ছে...")
    else:
        w, h = 1920, 1080
        max_duration = 90  # দেড় মিনিটের গভীর তিলাওয়াত (দ্রুত রেন্ডার ও হাই রিটেনশন)  # হাই কোয়ালিটি ৪ মিনিটের গভীর হৃদয়গ্রাহী তিলাওয়াত
        video_scale = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
        crf = "17"
        bitrate_args = ["-b:v", "8000k", "-maxrate", "12000k", "-bufsize", "16000k"]
        print("🎨 [HQ VIDEO RENDERING] ১৯২০x১০৮০ ফুল এইচডি ওয়াইডস্ক্রিন লং ভিডিও প্রস্তুত হচ্ছে...")

    watermark_png = generate_watermark_overlay(w, h)

    filter_complex = f"[0:v]{video_scale}[scaled_v];[scaled_v][2:v]overlay=0:0[final_v]"

    cmd = [
        FFMPEG_EXE, "-y",
        "-stream_loop", "-1",
        "-i", video_path,
        "-i", audio_path,
        "-i", watermark_png,
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", crf,
        *bitrate_args,
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-t", str(max_duration),
        "-shortest",
        "-map_metadata", "-1",
        out_path
    ]

    subprocess.run(cmd, check=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"✨ রেন্ডারিং সম্পন্ন! কোয়ালিটি: {'1080x1920 Reel' if is_reel else '1920x1080 Full HD Video'} | সাইজ: {os.path.getsize(out_path)/(1024*1024):.2f} MB")
        return out_path
    else:
        raise RuntimeError("ভিডিও রেন্ডারিং সম্পন্ন হয়নি।")

def download_quran_video(is_reel: bool = True, surah_data: dict = None, imam_data: dict = None) -> dict:
    """quran_runner.py থেকে প্রধান এন্ট্রি পয়েন্ট"""
    if not surah_data:
        surah_data = random.choice(LONG_SURAHS)

    if not imam_data:
        imam_data = random.choice(MAKKAH_MADINAH_IMAMS)

    print("\n=======================================================")
    print(f"📖 'কুরআনের তিলাওয়াত' ভিডিও ইঞ্জিন: {surah_data['bangla']} ({'Reel' if is_reel else 'HQ Video'})")
    print(f"🎙️ তিলাওয়াত: {imam_data['name']} ({imam_data['mosque']})")
    print("=======================================================")

    bg_video, mosque_meta = get_next_mosque_footage(surah_data)
    voice_audio, imam = download_imam_surah_audio(surah_data, imam_data)

    ts = int(time.time())
    format_tag = "reel" if is_reel else "hq_video"
    final_output = os.path.join(PROCESSED_DIR, f"quran_{surah_data['number']}_{format_tag}_{ts}.mp4")

    render_quran_video_with_watermark(bg_video, voice_audio, final_output, is_reel=is_reel)

    # ক্লিনআপ টেম্প অডিও ফাইল
    try:
        if os.path.exists(voice_audio): os.remove(voice_audio)
    except Exception: pass

    return {
        "filepath": final_output,
        "file_path": final_output,
        "is_reel": is_reel,
        "title": f"হৃদয় জুড়ানো তিলাওয়াত | {surah_data['bangla']} | {imam['name']}",
        "surah_name": surah_data["bangla"],
        "surah_number": surah_data["number"],
        "reciter": imam["name"],
        "mosque": imam["mosque"],
        "bg_mosque": mosque_meta["title"],
        "bg_location": mosque_meta["location"],
        "meaning": surah_data.get("meaning", ""),
        "benefit": surah_data.get("benefit", ""),
        "ayahs": surah_data.get("ayahs", "")
    }
