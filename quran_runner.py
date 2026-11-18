"""
Holy Quran 24/7 Automated Orchestrator & Runner
- ৫ ওয়াক্তের আজান অটোমেশন (ফজর, যোহর, আসর, মাগরিব, এশা)
- মক্কা ও মদিনার সকল ইমামগণের তিলাওয়াতসহ দৈনিক ২০+ লং সূরা পোস্ট
- পেজের স্থায়ী ব্র্যান্ডেড ওয়াটারমার্ক যুক্ত রিলস ও ভিডিও
- স্মার্ট অটো-কমেন্ট রেসপন্ডার (প্রাসঙ্গিক ইসলামিক দোয়া ও নো-ডুপ্লিকেট রিপ্লাই)
"""

import os
import sys
import json
import time
import random
import requests
import datetime

from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN
from quran_surah_database import MAKKAH_MADINAH_IMAMS, LONG_SURAHS
from quran_downloader import download_quran_video
from caption_engine import generate_quran_caption
from fb_video_uploader import upload_quran_video_to_page
from azan_engine import should_post_azan, post_daily_azan
from auto_comment_responder import run_comment_responder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_HISTORY_FILE = os.path.join(BASE_DIR, "posted_history.json")

def load_posted_history() -> dict:
    if os.path.exists(POSTED_HISTORY_FILE):
        try:
            with open(POSTED_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"posted_ids": data, "last_surah_index": -1, "last_imam_index": -1}
                elif isinstance(data, dict):
                    return data
        except Exception:
            return {"last_surah_index": -1, "last_imam_index": -1}
    return {"last_surah_index": -1, "last_imam_index": -1}

def save_posted_history(history: dict):
    try:
        with open(POSTED_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HISTORY WARN] {e}")

def get_next_surah_and_imam() -> tuple:
    """পরবর্তী সূরা ও মক্কা/মদিনার ইমাম নির্বাচন করে (যাতে প্রতিটি সূরা ও ইমাম সমান গুরুত্ব পান)"""
    history = load_posted_history()
    last_surah_index = history.get("last_surah_index", -1)
    last_imam_index = history.get("last_imam_index", -1)

    next_surah_index = (last_surah_index + 1) % len(LONG_SURAHS)
    next_imam_index = (last_imam_index + 1) % len(MAKKAH_MADINAH_IMAMS)

    selected_surah = LONG_SURAHS[next_surah_index]
    selected_imam = MAKKAH_MADINAH_IMAMS[next_imam_index]

    history["last_surah_index"] = next_surah_index
    history["last_imam_index"] = next_imam_index
    save_posted_history(history)

    return selected_surah, selected_imam

def run_single_quran_cycle():
    """১টি পূর্ণাঙ্গ চক্র: আজান চেক -> সূরা পাবলিশ -> অটো কমেন্ট রিপ্লাই"""
    print("\n========================================================")
    print("🚀 'কুরআনের তিলাওয়াত' অটোমেশন সাইকেল শুরু...")
    print("========================================================")

    # ধাপ ১: আজান চেক
    is_azan_time, waqt = should_post_azan()
    if is_azan_time:
        print(f"🕌 এখন {waqt.upper()} আজানের সময়! আজান পোস্ট তৈরি হচ্ছে...")
        res = post_daily_azan(waqt)
        print(f"✅ আজান সফলভাবে পোস্ট করা হয়েছে: {res}")
    else:
        # ধাপ ২: লং সূরা বা তিলাওয়াত ভিডিও পোস্ট
        selected_surah, selected_imam = get_next_surah_and_imam()
        print(f"📖 নির্বাচিত সূরা: {selected_surah['bangla']} ({selected_surah['arabic']})")
        print(f"🎙️ নির্বাচিত ইমাম: {selected_imam['name']} • {selected_imam['mosque']}")

        # ভিডিও ও অডিও প্রস্তুতকরণ (রিয়েল ফুটেজ ও ওয়াটারমার্ক সহ)
        video_metadata = download_quran_video(
            is_reel=True,
            surah_data=selected_surah,
            imam_data=selected_imam
        )

        video_path = video_metadata["filepath"]
        caption = generate_quran_caption(selected_surah, f"{selected_imam['name']} ({selected_imam['mosque']})", is_reel=True)
        title = f"{selected_surah['arabic']} • {selected_surah['bangla']} | {selected_imam['name']}"

        print("📤 ফেসবুকে ভিডিও আপলোড করা হচ্ছে...")
        upload_res = upload_quran_video_to_page(video_path, caption=caption, title=title)
        print(f"✅ সফল সূরা পোস্ট! রেজাল্ট: {upload_res}")

        # ক্লিনআপ
        if os.path.exists(video_path):
            try: os.remove(video_path)
            except Exception: pass

    # ধাপ ৩: স্মার্ট অটো-কমেন্ট রেসপন্ডার চালু
    try:
        run_comment_responder(page_type="quran", max_replies=10)
    except Exception as e:
        print(f"[COMMENT RESPONDER WARN] {e}")

if __name__ == "__main__":
    batch = 1
    if len(sys.argv) > 1:
        try:
            batch = int(sys.argv[1])
        except ValueError:
            batch = 1

    for i in range(batch):
        if i > 0:
            print("⏳ পরবর্তী ব্যাচের জন্য অপেক্ষা...")
            time.sleep(10)
        run_single_quran_cycle()
