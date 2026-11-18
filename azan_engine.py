"""
5 Waqt Viral Azan Automation Engine for 'কুরআনের তিলাওয়াত - Quran Tilawat' Page
বাংলাদেশ সময় অনুযায়ী ৫ ওয়াক্তের সময় পবিত্র মক্কা, মদিনা, আল-আকসা ও গ্র্যান্ড মসজিদের
১০০% আসল ও সিনেমাটিক ভিডিও ফুটেজ এবং বিশ্বখ্যাত আজানের মাধ্যমে স্বয়ংক্রিয়ভাবে ভিডিও পোস্ট করার ইঞ্জিন।
ভিডিওতে পেজের অফিশিয়াল ওয়াটারমার্ক সহ।
"""

import os
import re
import json
import time
import random
import datetime
import requests
import subprocess

from watermark_generator import generate_watermark_overlay
from fb_video_uploader import upload_quran_video_to_page

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
ASSETS_AZAN_DIR = os.path.join(BASE_DIR, "assets", "azan")
ASSETS_FOOTAGE_DIR = os.path.join(BASE_DIR, "assets", "footage")
AZAN_HISTORY_FILE = os.path.join(BASE_DIR, "azan_posted_today.json")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(ASSETS_AZAN_DIR, exist_ok=True)
os.makedirs(ASSETS_FOOTAGE_DIR, exist_ok=True)

# ৫ ওয়াক্তের নির্ভরযোগ্য ইসলামিক আজান অডিও এবং আসল মসজিদ ড্রোন ফুটেজ
AZAN_COLLECTION = {
    "fajr": {
        "name_bn": "ফজরের আজান",
        "name_ar": "أَذَانُ الْفَجْرِ",
        "place": "পবিত্র মক্কা মুকাররমা (মসজিদুল হারাম)",
        "muazzin": "শাইখ আলী আহমদ মুল্লা",
        "footage_file": "makkah_kaaba.mp4",
        "hadith": "রাসুলুল্লাহ (সা.) বলেছেন: যে ব্যক্তি ফজরের নামাজ জামাতে আদায় করল, সে যেন সারা রাত জেগে নামাজ পড়ল। (সহিহ মুসলিম)"
    },
    "dhuhr": {
        "name_bn": "যোহরের আজান",
        "name_ar": "أَذَانُ الظُّهْرِ",
        "place": "পবিত্র মদিনা মনোওয়ারা (মসজিদে নববী)",
        "muazzin": "শাইখ এসাম বুখারি",
        "footage_file": "madinah_nabawi.mp4",
        "hadith": "যোহরের পূর্বে চার রাকাত নামাজে আসমানের দরজাসমূহ খুলে দেওয়া হয়। (তিরমিযী)"
    },
    "asr": {
        "name_bn": "আসরের আজান",
        "name_ar": "أَذَانُ الْعَصْرِ",
        "place": "পবিত্র মক্কা মুকাররমা",
        "muazzin": "শাইখ মিশারি রশিদ আল-আফাসি",
        "footage_file": "makkah_kaaba.mp4",
        "hadith": "যে ব্যক্তি ফজর ও আসরের নামাজ যত্নসহকারে আদায় করবে, সে জান্নাতে প্রবেশ করবে। (সহিহ বুখারি)"
    },
    "maghrib": {
        "name_bn": "মাগরিবের আজান",
        "name_ar": "أَذَانُ الْمَغْرِبِ",
        "place": "পবিত্র মসজিদুল আকসা (বাইতুল মুকাদ্দাস)",
        "muazzin": "আল-আকসা মুয়াজ্জিন",
        "footage_file": "al_aqsa.mp4",
        "hadith": "মাগরিবের পর নফল নামাজ আদায়কারীদের জন্য মহান আল্লাহ বিশেষ নেয়ামত রেখেছেন।"
    },
    "isha": {
        "name_bn": "এশার আজান",
        "name_ar": "أَذَانُ الْعিশاءِ",
        "place": "পবিত্র মক্কা মুকাররমা",
        "muazzin": "শাইখ আলী আহমদ মুল্লা",
        "footage_file": "kaaba_rain.mp4",
        "hadith": "যে ব্যক্তি এশার নামাজ জামাতে আদায় করল, সে যেন অর্ধরাত দাঁড়িয়ে নামাজ আদায় করল। (সহিহ মুসলিম)"
    }
}

def get_current_bd_time():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    bd_now = utc_now + datetime.timedelta(hours=6)
    return bd_now

def get_current_waqt() -> str:
    """বর্তমান বাংলাদেশ সময় অনুযায়ী ওয়াক্ত নির্ধারণ করে"""
    bd_now = get_current_bd_time()
    hour = bd_now.hour
    minute = bd_now.minute

    # সময় উইন্ডো (BD Time)
    if (hour == 4 and minute >= 30) or (hour == 5 and minute <= 45):
        return "fajr"
    elif (hour == 11 and minute >= 45) or (hour == 12) or (hour == 13 and minute <= 30):
        return "dhuhr"
    elif (hour == 15 and minute >= 30) or (hour == 16 and minute <= 45):
        return "asr"
    elif (hour == 17 and minute >= 0) or (hour == 18 and minute <= 15):
        return "maghrib"
    elif (hour == 18 and minute >= 30) or (hour == 19) or (hour == 20 and minute <= 30):
        return "isha"

    return ""

def load_azan_history() -> dict:
    if os.path.exists(AZAN_HISTORY_FILE):
        try:
            with open(AZAN_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_azan_history(data: dict):
    try:
        with open(AZAN_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[AZAN WARN] {e}")

def should_post_azan() -> tuple:
    """চেক করে এখন কোনো ওয়াক্তের আজান পোস্ট করার উপযুক্ত সময় কিনা"""
    waqt = get_current_waqt()
    if not waqt:
        return False, ""

    bd_now = get_current_bd_time()
    today_str = bd_now.strftime("%Y-%m-%d")

    history = load_azan_history()
    posted_today = history.get(today_str, [])

    if waqt in posted_today:
        return False, waqt

    return True, waqt

def get_azan_audio_file(waqt: str) -> str:
    """লোকাল অ্যাসেট থেকে ভাইরাল আজানের অডিও প্রদান করে"""
    local_mp3 = os.path.join(ASSETS_AZAN_DIR, f"{waqt}.mp3")
    if os.path.exists(local_mp3) and os.path.getsize(local_mp3) > 10000:
        print(f"🎵 আজান অডিও লোড সম্পন্ন: {os.path.basename(local_mp3)} ({os.path.getsize(local_mp3)/(1024*1024):.2f} MB)")
        return local_mp3

    raise FileNotFoundError(f"আজান অডিও ফাইল পাওয়া যায়নি: {local_mp3}")

def get_azan_video_footage(waqt_data: dict) -> str:
    """লোকাল অ্যাসেট থেকে আসল সিনেমাটিক মসজিদ ফুটেজ প্রদান করে (মক্কা, মদিনা, আল-আকসা)"""
    file_name = waqt_data.get("footage_file", "makkah_kaaba.mp4")
    local_video = os.path.join(ASSETS_FOOTAGE_DIR, file_name)

    if os.path.exists(local_video) and os.path.getsize(local_video) > 50000:
        print(f"🎥 আসল সিনেমাটিক মসজিদ ফুটেজ লোড সম্পন্ন: {file_name} ({os.path.getsize(local_video)/(1024*1024):.2f} MB)")
        return local_video

    # ফলব্যাক হিসেবে উপস্থিত যে কোনো আসল মসজিদ ফুটেজ
    for alt in ["makkah_kaaba.mp4", "madinah_nabawi.mp4", "al_aqsa.mp4", "kaaba_rain.mp4"]:
        alt_path = os.path.join(ASSETS_FOOTAGE_DIR, alt)
        if os.path.exists(alt_path) and os.path.getsize(alt_path) > 50000:
            return alt_path

    raise FileNotFoundError(f"মসজিদ ভিডিও ফুটেজ পাওয়া যায়নি: {local_video}")

def render_azan_reel(video_path: str, audio_path: str, out_path: str) -> str:
    """
    আজান ভিডিও রিল রেন্ডার করে:
    - ১০০% আসল ড্রোন/সিনেমাটিক মসজিদ ফুটেজ
    - পেজ অফিশিয়াল ওয়াটারমার্ক (বাংলা + ইংরেজি নিখুঁত রেন্ডার)
    - ৯:১৬ ফুল এইচডি রিল
    """
    watermark_png = generate_watermark_overlay(720, 1280)
    video_scale = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
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
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "58",
        "-shortest",
        "-map_metadata", "-1",
        out_path
    ]

    subprocess.run(cmd, check=True)
    return out_path

def post_daily_azan(waqt: str) -> dict:
    """ওয়াক্ত অনুযায়ী আজান পোস্ট পাবলিশ করে"""
    waqt_data = AZAN_COLLECTION.get(waqt)
    if not waqt_data:
        return {"error": "Invalid waqt"}

    print(f"\n========================================================")
    print(f"🕌 আজান পাবলিশার শুরু: [{waqt_data['name_bn']}] - {waqt_data['place']}")
    print(f"========================================================")

    audio_path = get_azan_audio_file(waqt)
    video_path = get_azan_video_footage(waqt_data)
    ts = int(time.time())
    output_reel = os.path.join(DOWNLOADS_DIR, f"azan_{waqt}_{ts}.mp4")

    render_azan_reel(video_path, audio_path, output_reel)

    caption = (
        f"🕌 {waqt_data['name_bn']} | {waqt_data['place']}\n"
        f"🎙️ মুয়াজ্জিন: {waqt_data['muazzin']}\n\n"
        f"পবিত্র আজানের মধুর ধ্বনিতে অন্তরকে শান্ত করুন। 🤍\n"
        f"💡 {waqt_data['hadith']}\n\n"
        f"নামাজ কায়েম করুন, নিশ্চয় নামাজ সকল অশ্লীল ও পাপ কাজ থেকে বিরত রাখে। 🤲✨\n"
        f"ভিডিওটি শেয়ার করে সবাইকে নামাজের কথা স্মরণ করিয়ে দিন।\n\n"
        f"#Azan #{waqt.capitalize()}Azan #MakkahAzan #MadinaAzan #QuranTilawat #Namaz #IslamicReminder #PeaceOfMind"
    )
    title = f"{waqt_data['name_bn']} | {waqt_data['place']}"

    res = upload_quran_video_to_page(output_reel, caption=caption, title=title)

    # Mark as posted today
    bd_now = get_current_bd_time()
    today_str = bd_now.strftime("%Y-%m-%d")
    history = load_azan_history()
    history.setdefault(today_str, []).append(waqt)
    save_azan_history(history)

    # Clean up
    if os.path.exists(output_reel):
        try: os.remove(output_reel)
        except Exception: pass

    print(f"✅ সফল আজান পোস্ট সম্পন্ন! Result: {res}")
    return res
